from django.db import models
from tinymce.models import HTMLField
from django.core.mail import EmailMultiAlternatives, get_connection
from django.urls import reverse
from datetime import date, datetime
from members.models import Member
from django.contrib.postgres.fields.citext import CIEmailField
from solo.models import SingletonModel
from mxv.settings import LAUNCH_DATE
from review.models import Proposal
import re
from django.db.models.deletion import SET_NULL

# an email
place_holder_text = 'Available place-holders: [name], [link], [months_since_launch], [proposal_count] and [active_member_count]. '
logo_text = 'Use https://d3n8a8pro7vhmx.cloudfront.net/momentum/pages/92/attachments/original/1518443729/Momentum_logo_for_emails.png?1518443729 as the URL of an image to insert the Momentum logo.'
class Email(models.Model):
    name = models.CharField(max_length = 255, default = '')
    subject = models.CharField(max_length = 255)
    html_content = HTMLField(default = '', help_text = place_holder_text + logo_text )
    text_content = models.TextField(default = '', help_text = place_holder_text)
        
    def __str__(self):
        return self.name
    
    # sends the email to the test address
    def send_test(self, request):
        settings = EmailSettings.get_solo()
        return self.send_to(request, [settings.test_email_address])

    # sends the email to all inactive members
    def send_to_inactive_members(self, request):
        
        # get the inactive members
        inactive_members = Member.objects.filter(is_active = False)
        
        # send the emails
        return self.send_to(request, { member.email for member in inactive_members })
        
    # sends the email to the specified addresses
    def send_to(self, request, recipient_email_addresses):
        subject_template = self.place_holders_to_site_variables(self.subject)
        text_template = self.place_holders_to_site_variables(self.text_content)
        html_template = self.place_holders_to_site_variables(self.html_content)
        messages = []
        members = []
        for recipient_email_address in recipient_email_addresses:
            member = Member.objects.get(email=recipient_email_address)
            message = EmailMultiAlternatives(
                subject = subject_template, 
                body = self.place_holders_to_member_data(text_template, member, request),
                to = [recipient_email_address])
            message.attach_alternative(
                content = self.place_holders_to_member_data(html_template, member, request), 
                mimetype = "text/html")
            messages.append(message)
            members.append(member)
        connection = get_connection()
        connection.open()
        connection.send_messages(messages)
        connection.close()
        
        # track when the members were last sent an email
        for member in members:
            member.last_emailed = date.today()
            member.save()
        
        # return the number of members emailed
        return len(members)
    
    def place_holders_to_member_data(self, content, member, request):
        content = content.replace('[name]', member.name.split(' ')[0])
        link = request.build_absolute_uri(reverse('members:activate', kwargs = {'activation_key': member.activation_key}))
        content = content.replace('[link]', link)
        return content
        
    # replaces place-holders with site variables
    def place_holders_to_site_variables(self, content):
        content = content.replace('[months_since_launch]', '%d' % round((date.today() - LAUNCH_DATE).days / 30))   # months (kind of)
        content = content.replace('[active_member_count]', '{:,}'.format(Member.objects.filter(is_active=True).count()))
        content = content.replace('[proposal_count]', '{:,}'.format(Proposal.objects.count()))
        content = re.sub(r'(?P<date>\[days_to_[\w\s]+\])', days_to_yyyy_mm_dd, content)
        return content
        
    # sends the email to count inactive members who have not yet been invited
    def send_to_count_uninvited(self, request):
        settings = EmailSettings.get_solo()
        
        # get the inactive and uninvited members
        uninvited_members = Member.objects.filter(is_active = settings.is_active, last_emailed = None)
        uninvited_members_to_send = uninvited_members[:settings.send_count]
        
        # send the emails
        return self.send_to(request, { member.email for member in uninvited_members_to_send })
        
    # sends the email to count (in)active members who are email targets
    def send_to_count_targeted(self, request): 
        settings = EmailSettings.get_solo()
        
        # get the (in)active members
        members = Member.objects.filter(is_active = settings.is_active)
        
        # filter to those targeted but not yet sent (only send count)
        targets = EmailTarget.objects.filter(sent = None)[:settings.send_count]
        target_emails = { target.email for target in targets }
        targeted_members = members.filter(email__in=target_emails)
        
        # mark the targets as sent
        for target in targets:
            target.sent = True
            target.save()
        
        # send the emails
        count = self.send_to(request, { member.email for member in targeted_members })
        
        return count
        
# replaces [days_to_yyyy_mm_dd] tags with the number of days until that date
def days_to_yyyy_mm_dd(match):
    tag = match.group('date')
    tag = tag.replace('[days_to_', '').replace(']', '').replace('_', '/')
    tag_date = datetime.strptime(tag, '%Y/%m/%d')
    difference = tag_date - datetime.today()
    return str(difference.days + 1)
    
# email settings
class EmailSettings(SingletonModel):
    test_email_address = CIEmailField(default = '')
    send_count = models.PositiveIntegerField(default = 1000)
    is_active = models.BooleanField(default = False)
    activation_email = models.ForeignKey(Email, related_name = '+', blank = True, null = True, default = None, on_delete=SET_NULL)

# populate this table in SQL with email addresses to receive targeted emails
class EmailTarget(models.Model):
    email = CIEmailField(max_length=255, unique=True)
    sent = models.NullBooleanField(default=None)

# stores members that have re-consented to receive emails
class Reconsent(models.Model):
    email = CIEmailField(max_length=255, unique=True)
    reconsented_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    def __str__(self):
        return self.email

# default URL parameters that are copied to URL parameters when a model that uses them is created
class DefaultUrlParameter(models.Model):
    name = models.CharField(max_length = 100, help_text = 'The name of the URL parameter to pass on when redirecting')
    pass_on_name = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'Set this to pass the parameter on with a different name')
    nation_builder_value = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'The value for this parameter in the NationBuilder URL above')
    
    def __str__(self):
        return self.name
    
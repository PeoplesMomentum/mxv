from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from solo.models import SingletonModel
from tinymce.models import HTMLField
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

# creates members and super users
class MemberManager(BaseUserManager):
    
    # creates a member
    def create_member(self, email, name, password=None):

        if not email:
            raise ValueError('Members must have an email address')

        if not name:
            raise ValueError('Members must have a name')

        member = self.model(
            email = self.normalize_email(email),
            name = name
        )
        member.set_password(password)
        
        member.save(using=self._db)
        return member

    # creates a superuser
    def create_superuser(self, email, name, password):

        member = self.create_member(
            email,
            password = password,
            name = name
        )
        member.is_superuser = True
        member.is_active = True
        
        member.save(using=self._db)
        return member

# default to 20 digit activation keys
activation_key_length = 20
def activation_key_default():
    return Member.objects.make_random_password(length = activation_key_length)

# a member identified uniquely by their email address and publicly by their name 
class Member(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=activation_key_length, default=activation_key_default)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = MemberManager()

    # identify the member publicly by their name
    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name

    # debug
    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_superuser

# member activation email
class MemberActivationEmail(SingletonModel):
    subject = models.CharField(max_length = 255)
    html_content = HTMLField(default = '')
    text_content = models.TextField(default = '')
    test_email_address = models.EmailField(default = '')
    
    def __unicode__(self):
        return u"Member Activation Email"

    class Meta:
        verbose_name = "Member Activation Email"
        
    # sends the activation email to the test address
    def send_test(self, request):
        return self.send_to(request, [self.test_email_address])

    # sends the activation email to all inactive members
    def send_to_inactive_members(self, request):
        
        # get the inactive members
        inactive_members = Member.objects.filter(is_active = False)
        
        # send the emails
        return self.send_to(request, { member.email for member in inactive_members })
        
        pass

    # sends the activation email to the specified addresses
    def send_to(self, request, recipient_email_addresses):
        
        # create the message with the [name] and [link] place-holders replaced with Mailgun recipient variables
        message = EmailMultiAlternatives(
            subject = self.subject, 
            body = self.place_holders_to_Mailgun_recipient_variables(self.text_content),
            to = recipient_email_addresses)
        message.attach_alternative(
            content = self.place_holders_to_Mailgun_recipient_variables(self.html_content), 
            mimetype = "text/html")
        
        # get the members for the email addresses
        members = Member.objects.filter(email__in=recipient_email_addresses)
        
        # build the merge data for the recipients
        message.merge_data = { 
            member.email: { 
                'name': member.name, 
                'link': request.build_absolute_uri(reverse('members:activate', kwargs = {'activation_key': member.activation_key})) } 
            for member in members }
        
        # send the message to the recipients
        message.send()
        
        # return the number of members emailed
        return members.count() 

    
    # replaces place-holders with Mailgun recipient variables
    def place_holders_to_Mailgun_recipient_variables(self, content):
        content = content.replace('[name]', '%recipient.name%')
        content = content.replace('[link]', '%recipient.link%')
        return content
        

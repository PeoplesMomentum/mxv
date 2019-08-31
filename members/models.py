from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.contrib.postgres.fields.citext import CIEmailField
from enum import Enum
from solo.models import SingletonModel
from django.utils.crypto import get_random_string
from django.db.models.aggregates import Max

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

        # create the NationBuilder link (the new member might already be a supporter)
        supporter = NationBuilderPerson.objects.filter(email = email).first()
        if supporter:
            supporter.member = member
            supporter.save(using=self._db)
        else:
            NationBuilderPerson.objects.create(member = member, email = member.email)
        
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
    email = CIEmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=activation_key_length, default=activation_key_default)
    last_emailed = models.DateField(blank=True, null=True, default=None)
    is_ncg = models.BooleanField(default=False, verbose_name = 'NCG')
    is_members_council = models.BooleanField(default=False, verbose_name = "Members' council (can act on behalf of the member's council)")
    new_login_email = CIEmailField(max_length=255, blank=True, null=True, default=None)
    login_email_verification_key = models.CharField(max_length=activation_key_length, blank=True, null=True, default=None)

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

# returns a random token that has not yet been used as a unique token
# still vulnerable to race conditions from other web requests but better than assuming no collisions
unique_token_length = 20
def unused_unique_token():
    token = get_random_string(unique_token_length)
    while NationBuilderPerson.objects.filter(unique_token = token).first():
        token = get_random_string(unique_token_length)
    return token

# a member's link to their NationBuilder record
class NationBuilderPerson(models.Model):
    member = models.OneToOneField(Member, related_name = 'nation_builder_person', blank = True, null = True, default = None)
    email = CIEmailField(max_length=255, unique=True) # duplicate of member.email so that supporters can be promoted to members when joining
    unique_token = models.CharField(max_length = unique_token_length, default = unused_unique_token)
    nation_builder_id = models.IntegerField(blank=True, null=True, default=None)

    # debug
    def __str__(self):
        return '%s - %s (%s, %s)' % ('Member' if self.member else 'Supporter', self.email, self.unique_token, str(self.nation_builder_id) if self.nation_builder_id else '')

# UI choices for profile fields
class ProfileFieldType(Enum):
    Char = "Single line text"
    Integer = "Integer"
    Decimal = "Decimal"
    Boolean = "Checkbox (true/false)"
    Email = "Email"
    
# returns the next unused display order
def next_profile_field_display_order():
    highest = ProfileField.objects.aggregate(Max('display_order'))['display_order__max']
    return 1 if not highest else highest + 1

# fields in the members' NationBuilder records that are editable by the member on their profile page
class ProfileField(models.Model):
    field_path = models.CharField(max_length = 255)
    field_type = models.CharField(max_length = 8, choices = [(choice.name, choice.value) for choice in ProfileFieldType], default = ProfileFieldType.Char)
    required = models.BooleanField(default = False)
    display_text = models.CharField(max_length = 255, default = '')
    display_order = models.IntegerField(default = next_profile_field_display_order)
    admin_only = models.BooleanField(default = True)
    value_string = ''
    is_member_field = False
    
    # debug
    def __str__(self):
        return '%d - %s = %s' % (self.display_order, self.field_path, self.value_string)

# update details campaign
class UpdateDetailsCampaign(SingletonModel):
    second_page_pre_text = models.TextField()
    second_page_post_text = models.TextField()
    redirect_url = models.CharField(max_length = 255)
    
    # returns the URL parameters as the parameter string of a URL
    def url_parameter_string(self, request):
        url_parameters_present = []
        for url_parameter in self.url_parameters.all().order_by('name'):
            if url_parameter.name in request.GET:
                name = url_parameter.name if not url_parameter.pass_on_name or url_parameter.pass_on_name == '' else url_parameter.pass_on_name
                value = request.GET[url_parameter.name]
                url_parameters_present.append((name, value))
        url_parameter_string = '&'.join('='.join(present) for present in url_parameters_present)
        return url_parameter_string

# returns the next unused display order
def next_campaign_tag_group_display_order():
    highest = CampaignTagGroup.objects.aggregate(Max('display_order'))['display_order__max']
    return 1 if not highest else highest + 1
  
# a group of campaign tags
class CampaignTagGroup(models.Model):
    campaign = models.ForeignKey(UpdateDetailsCampaign, related_name = 'tag_groups')
    header = models.TextField()
    footer = models.TextField()
    display_order = models.IntegerField(default = next_campaign_tag_group_display_order)
      
    def __str__(self):
        return '%d' % self.display_order
  
# returns the next unused display order
def next_campaign_tag_display_order():
    highest = CampaignTag.objects.aggregate(Max('display_order'))['display_order__max']
    return 1 if not highest else highest + 1
  
# sets a tag in nation builder if checked by the member
class CampaignTag(models.Model):
    group = models.ForeignKey(CampaignTagGroup, related_name = 'tags')
    display_text = models.CharField(max_length = 255)
    tag = models.CharField(max_length = 255)
    display_order = models.IntegerField(default = next_campaign_tag_display_order)
    value_string = ''
      
    def __str__(self):
        return '%d - %s / %s = %s' % (self.display_order, self.display_text, self.tag, self.value_string)

# returns the next unused display order
def next_campaign_field_display_order():
    highest = CampaignField.objects.aggregate(Max('display_order'))['display_order__max']
    return 1 if not highest else highest + 1

# fields in the members' NationBuilder records that are editable by the member on the update details campaign page
class CampaignField(models.Model):
    campaign = models.ForeignKey(UpdateDetailsCampaign, related_name = 'fields')
    field_path = models.CharField(max_length = 255)
    field_type = models.CharField(max_length = 8, choices = [(choice.name, choice.value) for choice in ProfileFieldType], default = ProfileFieldType.Char)
    required = models.BooleanField(default = False)
    display_text = models.CharField(max_length = 255, default = '')
    display_order = models.IntegerField(default = next_campaign_field_display_order)
    value_string = ''
    
    # debug
    def __str__(self):
        return '%d - %s = %s' % (self.display_order, self.field_path, self.value_string)
    
# the URL parameters to pass on when redirecting 
# populated manually since the campaign is a singleton: 
#   insert into members_urlparameter (consultation_id, name, nation_builder_value) select 1, name, nation_builder_value from mxv_defaulturlparameter;
class UrlParameter(models.Model):
    consultation = models.ForeignKey(UpdateDetailsCampaign, related_name='url_parameters')
    name = models.CharField(max_length = 100, help_text = 'The name of the URL parameter to pass on when redirecting')
    pass_on_name = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'Set this to pass the parameter on with a different name')
    nation_builder_value = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'The value for this parameter in the NationBuilder URL above')
    
    def __str__(self):
        return self.name


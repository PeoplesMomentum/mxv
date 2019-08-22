from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.postgres.fields.citext import CIEmailField
from enum import Enum
from solo.models import SingletonModel

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
    email = CIEmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=activation_key_length, default=activation_key_default)
    last_emailed = models.DateField(blank=True, null=True, default=None)
    is_ncg = models.BooleanField(default=False, verbose_name = 'NCG')
    is_members_council = models.BooleanField(default=False, verbose_name = "Members' council (can act on behalf of the member's council)")
    nation_builder_id = models.IntegerField(blank=True, null=True, default=None)
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

# UI choices for profile fields
class ProfileFieldType(Enum):
    Char = "Single line text"
    Integer = "Integer"
    Decimal = "Decimal"
    Boolean = "Checkbox (true/false)"
    Email = "Email"

# fields in the members' NationBuilder records that are editable by the member on their profile page
class ProfileField(models.Model):
    # database fields
    field_path = models.CharField(max_length = 255)
    field_type = models.CharField(max_length = 8, choices = [(choice.name, choice.value) for choice in ProfileFieldType], default = ProfileFieldType.Char)
    required = models.BooleanField(default = False)
    display_text = models.CharField(max_length = 255, default = '')
    display_order = models.IntegerField(default = 1)
    admin_only = models.BooleanField(default = True)
    # runtime attributes
    value_string = ''
    is_member_field = False
    
    # debug
    def __str__(self):
        return '%s = %s' % (self.field_path, self.value_string)

# update details campaign
class UpdateDetailsCampaign(SingletonModel):
    first_page_pre_text = models.TextField()
    first_page_post_text = models.TextField()
    second_page_pre_text = models.TextField()
    second_page_post_text = models.TextField()
    redirect_URL = models.CharField(max_length = 255)
    
# sets a tag in nation builder if checked by the member
class CampaignTag(models.Model):
    campaign = models.ForeignKey(UpdateDetailsCampaign, related_name = 'tags')
    label = models.CharField(max_length = 255)
    tag = models.CharField(max_length = 255)
    display_order = models.IntegerField(default = 1)
    
    def __str__(self):
        return '%s / %s' % (self.label, self.tag)

# fields in the members' NationBuilder records that are editable by the member on the update details campaign page
class CampaignField(ProfileField):
    campaign = models.ForeignKey(UpdateDetailsCampaign, related_name = 'fields')
    


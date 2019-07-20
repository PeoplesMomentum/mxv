from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.postgres.fields.citext import CIEmailField
from enum import Enum

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

# UI choices for member-editable fields
class MemberEditableFieldType(Enum):
    Char = "Single line text"
    Text = "Multiple line text"
    Integer = "Integer"
    Decimal = "Decimal"
    Boolean = "Checkbox (true/false)"
    Email = "Email"
    Date = "Date"
    Time = "Time"
    DateTime = "Date and time"

# fields in the members' NationBuilder records that should be editable by the member on their profile page
class MemberEditableNationBuilderField(models.Model):
    field_path = models.CharField(max_length = 255)
    field_type = models.CharField(max_length = 8, choices = [(choice.name, choice.value) for choice in MemberEditableFieldType], default = MemberEditableFieldType.Char)
    required = models.BooleanField(default = False)
    display_text = models.CharField(max_length = 255, default = '')
    display_order = models.IntegerField(default = 1)
    admin_only = models.BooleanField(default = True)

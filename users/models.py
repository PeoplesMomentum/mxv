from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from solo.models import SingletonModel
from tinymce.models import HTMLField

# based mostly on https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#extending-the-existing-user-model

# creates users and super users
class UserManager(BaseUserManager):
    
    # creates a user
    def create_user(self, email, name, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            email = self.normalize_email(email),
            name = name
        )
        user.set_password(password)
        
        # generate an activation key
        user.activation_key = User.objects.make_random_password(length = 20)
        
        user.save(using=self._db)
        return user

    # creates a superuser
    def create_superuser(self, email, name, password):

        user = self.create_user(
            email,
            password = password,
            name = name
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_active = True
        
        user.save(using=self._db)
        return user

# a user identified uniquely by their email address and publicly by their name 
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=255, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()

    # identify the user publicly by their name
    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name

    # debug
    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin

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

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from solo.models import SingletonModel
from tinymce.models import HTMLField
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

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

# default to 20 digit activation keys
activation_key_length = 20
def activation_key_default():
    return User.objects.make_random_password(length = activation_key_length)

# a user identified uniquely by their email address and publicly by their name 
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=activation_key_length, default=activation_key_default)
    
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
        
    # sends the activation email to the test address
    def send_test(self, request):
        return self.send_to(request, [self.test_email_address])

    # sends the activation email to all inactive members
    def send_to_inactive_users(self, request):
        
        # get the inactive users
        inactive_users = User.objects.filter(is_active = False)
        
        # send the emails
        return self.send_to(request, { user.email for user in inactive_users })
        
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
        
        # get the users for the email addresses
        users = User.objects.filter(email__in=recipient_email_addresses)
        
        # build the merge data for the recipients
        message.merge_data = { 
            user.email: { 
                'name': user.name, 
                'link': request.build_absolute_uri(reverse('users:activate', kwargs = {'activation_key': user.activation_key})) } 
            for user in users }
        
        # send the message to the recipients
        message.send()
        
        # return the number of users emailed
        return users.count() 

    
    # replaces place-holders with Mailgun recipient variables
    def place_holders_to_Mailgun_recipient_variables(self, content):
        content = content.replace('[name]', '%recipient.name%')
        content = content.replace('[link]', '%recipient.link%')
        return content
        

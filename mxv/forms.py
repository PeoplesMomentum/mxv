from django import forms
from mxv.models import Reconsent, EmailSettings
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate
from members.models import Member
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator

class ReconsentForm(forms.ModelForm):    
    class Meta:
        model = Reconsent
        fields = ['email']

def SendActivationEmailToInactiveMember(request, email):

    # if the username relates to an inactive member...
    try:
        inactive_member = Member.objects.get(email = email, is_active = False)
    except:
        inactive_member = None
    if inactive_member:
        
        # send an activation email
        activation_email = EmailSettings.get_solo().activation_email
        if activation_email:
            try:
                activation_email.send_to(request, [inactive_member.email])
            except:
                pass
class ActivationEmailAuthenticationForm(AuthenticationForm):
    
    # gets the request
    def __init__(self, *args, **kwargs):
        super(ActivationEmailAuthenticationForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)

    # copied from AuthenticationForm but modified to send an activation email to inactive members
    def clean(self):
        
        # if the username/password are present...
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            
            # but not valid...
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                
                # send an activation email if inactive member
                SendActivationEmailToInactiveMember(self.request, username)
                
                # raise the invalid login error
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                # allow further checks on the user
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class EmailForm(forms.Form):    
    email = forms.EmailField()

class ActivationEmailPasswordResetForm(PasswordResetForm):
    
    # sends an activation email if the email relates to an inactive member
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        
        email = self.cleaned_data["email"]

        # send an activation email if inactive member
        SendActivationEmailToInactiveMember(request, email)
              
        # usual logic
        super(ActivationEmailPasswordResetForm, self).save(domain_override, 
                                                           subject_template_name, 
                                                           email_template_name, 
                                                           use_https, 
                                                           token_generator, 
                                                           from_email, 
                                                           request, 
                                                           html_email_template_name, 
                                                           extra_email_context)


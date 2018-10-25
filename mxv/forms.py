from django import forms
from mxv.models import Reconsent, EmailSettings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from members.models import Member
from django.contrib import messages

class ReconsentForm(forms.ModelForm):    
    class Meta:
        model = Reconsent
        fields = ['email']

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
                
                # if the username relates to an inactive member...
                try:
                    inactive_member = Member.objects.get(email = username, is_active = False)
                except:
                    inactive_member = None
                if inactive_member:
                    
                    # send an activation email
                    activation_email = EmailSettings.get_solo().activation_email
                    if activation_email:
                        try:
                            activation_email.send_to(self.request, [inactive_member.email])
                        except:
                            pass
             
                # always notify that an activation email might have been sent
                messages.info(self.request, 'If you’re a member but haven’t activated your account yet then you’ve been sent an activation email (so check your email inbox and spam folders)')

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

class RequestActivationEmailForm(forms.Form):    
    email = forms.EmailField()



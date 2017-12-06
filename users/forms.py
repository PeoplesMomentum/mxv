from django import forms
from .models import MemberActivationEmail

# form for editing member activation email
class MemberActivationEmailForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'size':65}))
    test_email_address = forms.CharField(widget=forms.TextInput(attrs={'size':56}))
    class Meta:
        model = MemberActivationEmail
        fields = ['subject', 'content', 'test_email_address']

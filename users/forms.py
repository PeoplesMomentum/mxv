from django import forms
from .models import MemberActivationEmail

# form for editing member activation email
class EditMemberActivationEmailForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'size':65}))
    class Meta:
        model = MemberActivationEmail
        fields = ['subject', 'content']

# form for sending member activation email
class SendMemberActivationEmailsForm(forms.ModelForm):
    test_email_address = forms.CharField(widget=forms.TextInput(attrs={'size':65}))
    class Meta:
        model = MemberActivationEmail
        fields = ['test_email_address']

# form for importing member names and email addresses
class ImportMemberNamesAndEmailAddressesForm(forms.Form):
    csv = forms.FileField()

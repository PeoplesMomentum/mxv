from django import forms
from mxv.models import EmailSettings

# form for sending member activation email
class SendMemberActivationEmailsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = ['test_email_address', 'send_count', 'is_active', 'activation_email']
        widgets = {
            'test_email_address': forms.TextInput(attrs={'size':65})}

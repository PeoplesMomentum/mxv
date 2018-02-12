from django import forms
from .models import MemberActivationEmail

# form for editing member activation email
class EditMemberActivationEmailForm(forms.ModelForm):
    class Meta:
        model = MemberActivationEmail
        fields = ['subject', 'html_content', 'text_content']
        widgets = {
            'subject': forms.TextInput(attrs={'size':65}),
            'text_content': forms.Textarea(attrs={'rows':10, 'cols':60})}

# form for sending member activation email
class SendMemberActivationEmailsForm(forms.ModelForm):
    class Meta:
        model = MemberActivationEmail
        fields = ['test_email_address', 'send_count', 'is_active']
        widgets = {
            'test_email_address': forms.TextInput(attrs={'size':65})}

# form for importing member names and email addresses
class ImportMemberNamesAndEmailAddressesForm(forms.Form):
    csv = forms.FileField()

from django import forms
from .models import MemberActivationEmail

# form for editing member activation email
class MemberActivationEmailForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'size':65}))
    class Meta:
        model = MemberActivationEmail
        fields = ['subject', 'content']

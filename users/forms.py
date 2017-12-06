from django.forms import ModelForm
from .models import MemberActivationEmail

# form for editing member activation email
class MemberActivationEmailForm(ModelForm):
    class Meta:
        model = MemberActivationEmail
        fields = ['subject', 'content']

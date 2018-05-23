from django import forms
from mxv.models import Reconsent

class ReconsentForm(forms.ModelForm):    
    class Meta:
        model = Reconsent
        fields = ['email']

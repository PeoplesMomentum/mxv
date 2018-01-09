from django import forms
from .models import Proposal, text_length

class NewProposalForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'placeholder': "Choose a name for your proposal" }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'rows': 5, 'placeholder': "What is your proposal?" }), 
        max_length = text_length, 
        help_text = "The maximum length of the text is %d" % text_length)

    class Meta:
        model = Proposal
        fields = ['name', 'text']
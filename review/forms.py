from django import forms
from .models import Proposal, text_length, Amendment, Comment

class ProposalForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'disabled': True }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'disabled': True, 'rows': 5 }))

    class Meta:
        model = Proposal
        fields = ['name', 'text']

class EditProposalForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'placeholder': "Choose a name for your proposal" }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'rows': 5, 'placeholder': "What is your proposal?" }), 
        max_length = text_length, 
        help_text = "The maximum length of the text is %d" % text_length)

    class Meta:
        model = Proposal
        fields = ['name', 'text']
        
class DeleteProposalForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'readonly': True }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': 5 }))
     
    class Meta:
        model = Proposal
        fields = ['name', 'text']

class AmendmentForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'disabled': True }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'disabled': True, 'rows': 5 }))

    class Meta:
        model = Amendment
        fields = ['name', 'text']

class EditAmendmentForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'placeholder': "Choose a name for your amendment" }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'rows': 5, 'placeholder': "What is your amendment?" }), 
        max_length = text_length, 
        help_text = "The maximum length of the text is %d" % text_length)

    class Meta:
        model = Amendment
        fields = ['name', 'text']

class DeleteAmendmentForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'readonly': True }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': 5 }))
     
    class Meta:
        model = Amendment
        fields = ['name', 'text']

class EditCommentForm(forms.ModelForm):
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'rows': 5, 'placeholder': "What is your comment?" }), 
        max_length = text_length, 
        help_text = "The maximum length of the text is %d" % text_length)

    class Meta:
        model = Comment
        fields = ['text']


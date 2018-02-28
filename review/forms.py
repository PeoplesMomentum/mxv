from django import forms
from .models import Proposal, Amendment, Comment, ModerationRequest, Vote, name_length, text_length, summary_length

TEXT_FIELD_ROWS = 8

class ProposalForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'readonly': True }))
    summary = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': TEXT_FIELD_ROWS }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': TEXT_FIELD_ROWS }))

    class Meta:
        model = Proposal
        fields = ['name', 'summary', 'text']

class EditProposalForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'placeholder': "Choose a name for your proposal" }),
        max_length = name_length,
        help_text = "The maximum length of the name is %d characters" % name_length)
    summary = forms.CharField(
        widget = forms.Textarea(attrs = { 'rows': TEXT_FIELD_ROWS, 'placeholder': "Please summarise your proposal" }), 
        max_length = summary_length, 
        help_text = "The maximum length of the text is %d characters" % summary_length)
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'rows': TEXT_FIELD_ROWS, 'placeholder': "What is the full text of your proposal?" }), 
        max_length = text_length, 
        help_text = "The maximum length of the text is %d characters" % text_length)

    class Meta:
        model = Proposal
        fields = ['name', 'summary', 'text']
        
class DeleteProposalForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'readonly': True }))
    summary = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': TEXT_FIELD_ROWS }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': TEXT_FIELD_ROWS }))
     
    class Meta:
        model = Proposal
        fields = ['name', 'summary', 'text']

class AmendmentForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'readonly': True }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': TEXT_FIELD_ROWS }))

    class Meta:
        model = Amendment
        fields = ['name', 'text']

class EditAmendmentForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'placeholder': "Choose a name for your amendment" }),
        max_length = name_length,
        help_text = "The maximum length of the name is %d characters" % name_length)
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'rows': TEXT_FIELD_ROWS, 'placeholder': "What is your amendment?" }), 
        max_length = text_length, 
        help_text = "The maximum length of the text is %d characters" % text_length)

    class Meta:
        model = Amendment
        fields = ['name', 'text']

class DeleteAmendmentForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs = { 'readonly': True }))
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': TEXT_FIELD_ROWS }))
     
    class Meta:
        model = Amendment
        fields = ['name', 'text']

class EditCommentForm(forms.ModelForm):
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'rows': TEXT_FIELD_ROWS, 'placeholder': "What is your comment?" }), 
        max_length = text_length, 
        help_text = "The maximum length of the text is %d characters" % text_length)

    class Meta:
        model = Comment
        fields = ['text']

class ModerationRequestForm(forms.ModelForm):
    def __init__(self, entity, *args,**kwargs):
        super(ModerationRequestForm, self).__init__(*args, **kwargs)
        self.fields['reason'] = forms.CharField(
            widget = forms.Textarea(attrs = { 'rows': TEXT_FIELD_ROWS, 'placeholder': "Why does this %s require moderation?" % entity }), 
            max_length = text_length, 
            help_text = "The maximum length of the reason is %d characters" % text_length)

    class Meta:
        model = ModerationRequest
        fields = ['reason']

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget = forms.Textarea(attrs = { 'readonly': True, 'rows': TEXT_FIELD_ROWS }))

    class Meta:
        model = Comment
        fields = ['text']

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = []


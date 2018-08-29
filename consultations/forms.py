from django import forms
from consultations.models import Vote

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = []

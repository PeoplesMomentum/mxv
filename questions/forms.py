from django import forms
from questions.models import Question, Answer, Candidate

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'text']
        widgets = {
          'text': forms.Textarea(attrs={'rows':6, 'cols':50}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
          'text': forms.Textarea(attrs={'rows':10, 'cols':50}),
        }


class PositionForm(forms.Form):
    position = forms.ChoiceField(choices=Candidate.POSITION_CHOICES, widget=forms.Select(attrs={"onchange": "this.form.submit()"}))
    question = forms.ModelChoiceField(queryset=Question.objects.filter(status='approved'), widget=forms.HiddenInput())

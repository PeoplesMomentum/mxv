from django import forms
from questions.models import Question, Answer

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

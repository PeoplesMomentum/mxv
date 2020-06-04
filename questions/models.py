from django.core.exceptions import ValidationError
from django.db import models
from mxv.settings import AUTH_USER_MODEL

class Candidate(models.Model):
    member = models.OneToOneField(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    candidate_code = models.CharField(max_length=16)
    POSITION_CHOICES = [
        ('nww', 'North West and Wales'),
        ('sesw', 'South East and South West'),
        ('mide', 'Midlands and the East'),
        ('lon', 'London'),
        ('ysn', 'Yorkshire and the Humber, Cumbria, North East, Scotland, and International'),
        ('mper', 'MPs and elected representatives')
    ]
    position = models.CharField(max_length=6, choices=POSITION_CHOICES)

    def __str__(self):
        return f'{self.member.name} - {self.position}'


class Category(models.Model):
    number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255)
  
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ('number',)

    def __str__(self):
        return f'{self.number}. {self.title}'


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
]

def text_length(text, name, maxlen):
    textlen = len(text.split())
    if textlen > maxlen:
        raise ValidationError(f'{name}s are limited to {maxlen} words; you had {textlen}')

def question_length(text):
    text_length(text, 'Question', 40)

def answer_length(text):
    text_length(text, 'Answer', 200)


class Question(models.Model):
    text = models.TextField(max_length=255, validators=[question_length], help_text="Maximum 40 words")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='pending', choices=STATUS_CHOICES, max_length=16)
    answers = models.ManyToManyField(Candidate, through='Answer')
    votes = models.ManyToManyField(AUTH_USER_MODEL, through='Vote')
    reject_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.category.number}. {self.text}'


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    member = models.ForeignKey(AUTH_USER_MODEL, related_name='question_votes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Upvote by {self.member.email}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    text = models.TextField(max_length=2048, validators=[answer_length], help_text="Maximum 200 words")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='pending', choices=STATUS_CHOICES, max_length=16)
    reject_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.question.text[:20]} - {self.text}'

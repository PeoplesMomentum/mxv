from django.db import models
from mxv.settings import AUTH_USER_MODEL
from datetime import date
from django.utils import formats
from django.db.models.deletion import CASCADE
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from mxv.models import DefaultUrlParameter

# field sizes
short_text_length = 255
long_text_length = 2000

# a consultation
class Consultation(models.Model):
    template = models.CharField(max_length=short_text_length, blank=True, null=True, default=None)
    name = models.CharField(max_length=short_text_length, unique=True)
    description = models.TextField(max_length=short_text_length)
    pre_questions_text = models.TextField(max_length=long_text_length, blank=True, null=True, default=None)
    post_questions_text = models.TextField(max_length=long_text_length, blank=True, null=True, default=None)
    voting_start = models.DateField()
    voting_end = models.DateField()
    visible_to_non_staff = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=1)
    hide_results = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    # whether voting is currently allowed
    def voting_in_range(self):
        today = date.today()
        return today >= self.voting_start and today <= self.voting_end
    
    # description of voting dates
    def voting_date_text(self):
        if self.voting_end >= date.today():
            return '%s - %s' % (formats.date_format(self.voting_start, 'd/m/Y'), formats.date_format(self.voting_end, 'd/m/Y'))
        else:
            return 'Completed'
        
    # voting guidance
    def guidance(self):
        today = date.today()
        if today < self.voting_start:
            return 'Voting on this consultation will be starting on %s.' % formats.date_format(self.voting_start, 'l jS F')
        elif self.voting_in_range():
            return 'Voting on this consultation is now live.'
        else:
            return 'Voting on this consultation has ended.'
    
    # voting guidance CSS
    def guidance_class(self):
        if self.voting_in_range():
            return 'text-danger'
        else:
            return 'text-muted'
        
    # voting button
    def vote_button_text(self):
        today = date.today()
        if today < self.voting_start:
            return 'View questions'
        elif self.voting_in_range():
            return 'Vote now'
        else:
            return 'View results'
        
    # questions in number order
    def questions_in_number_order(self):
        return self.questions.order_by('number')
    
    # returns the URL parameters as the parameter string of a URL
    def url_parameter_string(self, request):
        url_parameters_present = []
        for url_parameter in self.url_parameters.all().order_by('name'):
            if url_parameter.name in request.GET:
                name = url_parameter.name if not url_parameter.pass_on_name or url_parameter.pass_on_name == '' else url_parameter.pass_on_name
                value = request.GET[url_parameter.name]
                url_parameters_present.append((name, value))
        url_parameter_string = '&'.join('='.join(present) for present in url_parameters_present)
        return url_parameter_string

    
# a question on a consultation
class Question(models.Model):
    consultation = models.ForeignKey(Consultation, related_name='questions', on_delete=CASCADE)
    number = models.PositiveIntegerField()
    text = models.TextField(max_length=long_text_length)
    guidance = models.TextField(max_length=long_text_length, default='', blank=True)
    multipleAnswersAllowed = models.BooleanField(verbose_name = 'Multiple answers allowed')

    def __str__(self):
        return '%d - %s' % (self.number, self.text)

# a possible answer to a question
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=CASCADE)
    display_order = models.PositiveIntegerField(default=1)
    text = models.CharField(max_length=short_text_length)
    redirect_url = models.CharField(max_length=short_text_length, blank=True, null=True, default=None)

    def __str__(self):
        return self.text

class Vote(models.Model):
    consultation = models.ForeignKey(Consultation, related_name='votes', on_delete=CASCADE)
    member = models.ForeignKey(AUTH_USER_MODEL, related_name='consultation_votes', on_delete=CASCADE)

    def __str__(self):
        return '%s / %s' % (self.consultation, self.member)
    
# a member's answer to a question
class Answer(models.Model):
    vote = models.ForeignKey(Vote, related_name='answers', on_delete=CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=CASCADE)
    choice = models.ForeignKey(Choice, related_name='answers', on_delete=CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s / %s' % (self.question, self.choice)

# the URL parameters to pass on when redirecting
class UrlParameter(models.Model):
    consultation = models.ForeignKey(Consultation, related_name='url_parameters', on_delete=CASCADE)
    name = models.CharField(max_length = 100, help_text = 'The name of the URL parameter to pass on when redirecting')
    pass_on_name = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'Set this to pass the parameter on with a different name')
    nation_builder_value = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'The value for this parameter in the NationBuilder URL above')
    
    def __str__(self):
        return self.name

# adds the default URL parameters to new consultations
@receiver(post_save, sender = Consultation)
def add_default_url_parameters(sender, instance, created, *args, **kwargs):
    if created:
        for param in DefaultUrlParameter.objects.all():
            UrlParameter.objects.create(consultation = instance, name = param.name, pass_on_name = param.pass_on_name, nation_builder_value = param.nation_builder_value)


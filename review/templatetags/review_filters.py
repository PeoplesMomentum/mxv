from django import template
from django.utils.safestring import mark_safe
from datetime import date

register = template.Library()

# returns the requested question and choice HTML
@register.filter()
def question_and_choices(vote, question_id):
    
    # question
    question_count = vote.track_voting.questions.count()
    question = vote.track_voting.questions.filter(pk=question_id).first()
    question_html = 'Question %d of %d - %s' % (question.number, question_count, question.text)

    # answer        
    current_answer = vote.answers.filter(question = question).first()

    # choices
    choices = question.choices.all()
    today = date.today()
    choice_html = ''
    
    # voting not started
    if vote.track_voting.voting_start > today:
        choice_html = '<label class="mt-4">[Voting not yet started]</label>'
        
    # voting in progress
    elif vote.track_voting.voting_in_range():
        for choice in choices:
            choice_html += '<label class="radio-inline mt-4 mr-4"><input type="radio" name="answer_%d" value="%d_%d" %s>%s</label>' % (question.id, question.id, choice.id, 'checked="checked"' if current_answer and current_answer.choice == choice else '', choice.text)
    
    # voting complete
    else:
        # vote counts
        for choice in choices:
            choice_count = choice.answers.filter(question__pk = question_id).count()
            choice_html += '<label class="mt-4 mr-4">%s - %d vote%s</label>' % (choice.text, choice_count, '' if choice_count == 1 else 's')
        
        # member's choice
        if current_answer:
            choice_html += '<label class="mt-4 mr-4">(You voted %s)</label>' % current_answer.choice.text
        else:
            choice_html += '<label class="mt-4 mr-4">(You didn''t vote on this question)</label>'
          
    # layout    
    return mark_safe("""
        <p><em>
            %s
            <br/>
            <span class="ml-4">%s</span>
        </em></p>
        """ % (question_html, choice_html))

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
        
    # choices
    choices = question.choices.all()
    today = date.today()
    choice_html = ''
    
    # voting not started
    if vote.track_voting.voting_start > today:
        choice_html = '<label class="mt-4">[Voting not yet started]</label>'
        
    # voting in progress
    elif vote.track_voting.voting_in_range():
        current_answer = vote.answers.filter(question = question).first()
        for choice in choices:
            choice_html += '<label class="radio-inline mt-4 mr-4"><input type="radio" name="answer" value="%d_%d" %s>%s</label>' % (question.id, choice.id, 'checked="checked"' if current_answer and current_answer.choice == choice else '', choice.text)
    
    # voting complete
    else:
        for choice in choices:
            choice_html += '<label class="mt-4 mr-4">%s - %d votes</label>' % (choice.text, choice.answers.filter(question__pk = question_id).count())
    
    # vote
    vote_html = '<button type="submit" name="vote" class="btn btn-primary">Update votes</button>' if vote.track_voting.voting_in_range() else ''
          
    # layout    
    return mark_safe("""
        <p><em>
            %s
            <br/>
            <span class="ml-4">%s</span><span>%s</span>
        </em></p>
        """ % (question_html, choice_html, vote_html))

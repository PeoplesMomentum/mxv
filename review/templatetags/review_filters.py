from django import template
from django.utils.safestring import mark_safe
from datetime import date

register = template.Library()

# returns the requested question and choice HTML
@register.filter()
def question_and_choices(voting_context, question_id):
    
    # question
    question_count = voting_context.track_voting.questions.count()
    question = voting_context.track_voting.questions.filter(pk=question_id).first()
    question_html = '<strong>Question %d of %d</strong> - %s' % (question.number, question_count, question.text)

    # answer        
    current_answer = None
    if voting_context.vote:
        current_answer = voting_context.vote.answers.filter(question = question).first()

    # choices
    choices = question.choices.all()
    today = date.today()
    choice_html = ''
    
    # voting not started
    if voting_context.track_voting.voting_start > today:
        choice_html = '<label class="mt-4">[Voting not yet started]</label>'
        
    # voting in progress
    elif voting_context.track_voting.voting_in_range():
        if not voting_context.request.user.is_anonymous:
            for choice in choices:
                choice_html += '<label class="radio-inline mt-4 mr-4"><input type="radio" name="answer_%d" value="%d_%d" %s>%s</label>' % (question.id, question.id, choice.id, 'checked="checked"' if current_answer and current_answer.choice == choice else '', choice.text)
        else:
            choice_html = '<label class="mt-4">[Log in to vote]</label>'
    
    # voting complete
    else:
        # results
        for choice in choices:
            count = question.answers.filter(choice = choice).count()
            total = question.answers.count()
            choice_html += '<label class="mt-4 mr-4">%d voted %s (%d%%)</label>' % (count, choice.text, count / total * 100 if total > 0 else 0)
        
        # answer
        if current_answer:
            choice_html += '<label class="mt-4 mr-4">(You voted %s)</label>' % current_answer.choice.text
        elif not voting_context.request.user.is_anonymous:
            choice_html += '<label class="mt-4 mr-4">(You didn\'t vote on this question)</label>'
          
    # layout    
    return mark_safe("""
        <p><em>
            <span class="question-text">%s</span>
            <br/>
            <span class="ml-4">%s</span>
        </em></p>
        """ % (question_html, choice_html))

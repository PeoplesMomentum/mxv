from django import template
from django.utils.safestring import mark_safe
from datetime import date

register = template.Library()

def comma_and(elements):
    if len(elements) == 0:
        return ''
    if len(elements) == 1:
        return elements[0]
    if len(elements) == 2:
        return ' and '.join(elements)
    else:
        return ' and '.join([', '.join(elements[:-1]), elements[-1]])

# returns the requested question and choice HTML
@register.filter()
def question_and_choices(voting_context, question_id):
    
    # question
    question_count = voting_context.consultation.questions.count()
    question = voting_context.consultation.questions.filter(pk=question_id).first()
    question_html = '<strong>Question %d of %d</strong> - %s' % (question.number, question_count, question.text)
    if question.guidance != "":
        question_html += '<p class="ml-4">%s</p>' % question.guidance

    # answers
    current_answers = []
    if voting_context.vote:
        current_answers = voting_context.vote.answers.filter(question = question).all()

    # choices
    choices = question.choices.all().order_by('display_order')
    today = date.today()
    choice_html = '<br/>'
    
    # voting not started
    if voting_context.consultation.voting_start > today:
        choice_html += '<br/><label>[Voting not yet started]</label>'
        
    # voting in progress
    elif voting_context.consultation.voting_in_range():
        if not voting_context.request.user.is_anonymous():
            for choice in choices:
                if question.multipleAnswersAllowed:
                    choice_html += '<label class="checkbox-inline ml-4"><input type="checkbox" class="mr-4" name="answer_%d" value="%d_%d" %s>%s</label><br/>' % (question.id, question.id, choice.id, 'checked="checked"' if choice in [answer.choice for answer in current_answers] else '', choice.text)
                else:
                    choice_html += '<label class="radio-inline ml-4"><input type="radio" class="mr-4" name="answer_%d" value="%d_%d" %s>%s</label><br/>' % (question.id, question.id, choice.id, 'checked="checked"' if choice in [answer.choice for answer in current_answers] else '', choice.text)
        else:
            choice_html += '<label class="ml-4">[Log in to vote]</label>'
    
    # voting complete
    else:
        # results
        choice_html += '<br/>'
        for choice in choices:
            count = question.answers.filter(choice = choice).count()
            total = question.answers.count()
            choice_html += '<label class="ml-4">%d voted \'%s\' (%d%%)</label><br/>' % (count, choice.text, count / total * 100 if total > 0 else 0)
        
        # answers
        choice_html += '<br/>'
        if len(current_answers) > 0:
            choice_html += '<label class="ml-4">[You voted %s]</label><br/>' % comma_and(['\'%s\'' % answer.choice.text for answer in current_answers])
        elif not voting_context.request.user.is_anonymous():
            choice_html += '<label class="ml-4">[You didn\'t vote on this question]</label><br/>'
          
    # layout    
    return mark_safe("""
        <p><em>
            <span class="question-text">%s</span>
            %s
        </em></p>
        """ % (question_html, choice_html))

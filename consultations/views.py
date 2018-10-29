from django.shortcuts import render, get_object_or_404, redirect
from consultations.models import Consultation
from mxv.settings import CONSULTATIONS_VISIBLE_TO_NON_STAFF
from consultations.forms import VoteForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# renders the consultations index
@login_required
def index(request):
    # redirect if consultations not allowed yet for non-staff
    if not (CONSULTATIONS_VISIBLE_TO_NON_STAFF or request.user.is_staff):
        return redirect('index')
    
    # filter by whether visible to staff
    if request.user.is_staff:
        consultations = Consultation.objects.all()
    else:
        consultations = Consultation.objects.filter(visible_to_non_staff=True).all()
    
    return render(request, 'consultations/consultations.html', { 
        'consultations': consultations })

# encapsulates request, vote and consultation for when there is no vote (i.e. anonymous user)
class VotingContext:
    request = None
    vote = None
    consultation = None

# renders a single consultation (currently only for members but can remove the login_required decorator to allow anonymous)
@login_required
def consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk = pk)
    
    # redirect if consultations not allowed yet for non-staff
    if not (CONSULTATIONS_VISIBLE_TO_NON_STAFF or request.user.is_staff):
        return redirect('index')
    
    # redirect if this consultation is not allowed for non-staff
    if not (consultation.visible_to_non_staff or request.user.is_staff):
        return redirect('index')
    
    # if there is a logged-in member...
    if not request.user.is_anonymous():

        # ensure there is a vote for the member
        vote = request.user.consultation_votes.filter(consultation = consultation).first()
        if not vote:
            vote = consultation.votes.create(member = request.user)
        
        # if valid post CRSF token and voting is currently allowed...
        if request.method == 'POST' and consultation.voting_in_range():
            form = VoteForm(request.POST)
            if form.is_valid():
                
                # and it's a vote ...
                if 'vote' in request.POST:
                    
                    # delete old answers
                    vote.answers.all().delete()
                    
                    # for each answer...
                    for answer_key in [key for key in request.POST.keys() if key.startswith('answer_')]:
                        try:
                            # for each choice...
                            post_answers = request.POST.getlist(answer_key)
                            for post_answer in post_answers:
                            
                                # get the question and choice
                                (question_id, choice_id) = post_answer.split('_')
                                question = consultation.questions.filter(id = question_id).first()
                                choice = question.choices.filter(id = choice_id).first()
                                    
                                # add new answer
                                vote.answers.create(question = question, choice = choice)
                        except:
                            pass                    
                
                # redirect to a custom URL if specified by a choice (for the last question if more than one are specified)
                redirect_url = ''
                for answer in vote.answers.order_by('question__number'):
                    if answer.choice.redirect_url != '':
                        redirect_url = answer.choice.redirect_url
                if redirect_url != '':
                    return redirect(redirect_url)
                    
                # redirect to thanks page if no choice-specific redirect URL
                return redirect('consultations:thanks', pk = consultation.pk)
            else:
                # show errors
                messages.error(request, 'Please correct the errors below.')
        else:
            # get or invalid post
            form = VoteForm(instance = vote)
    else:
        # not logged in
        vote = None
        form = VoteForm()

    voting_context = VotingContext()
    voting_context.request = request
    voting_context.vote = vote
    voting_context.consultation = consultation
    return render(request, 'consultations/consultation.html', { 
        'voting_context': voting_context, 
        'form': form })

# shown after voting
@login_required
def thanks(request, pk):
    consultation = get_object_or_404(Consultation, pk = pk)
    return render(request, 'consultations/thanks.html', { 
        'consultation': consultation })
    
    

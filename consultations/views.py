from django.shortcuts import render, get_object_or_404, redirect
from consultations.models import Consultation
from mxv.settings import CONSULTATIONS_VISIBLE_TO_NON_STAFF
from consultations.forms import VoteForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse


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
        
    # set display order
    consultations = consultations.order_by('display_order')
    
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
                redirect_url = None
                for answer in vote.answers.order_by('question__number'):
                    if answer.choice.redirect_url != None and answer.choice.redirect_url != '':
                        redirect_url = answer.choice.redirect_url
                if redirect_url != None:
                    # redirect with URL parameters
                    url_parameter_string = consultation.url_parameter_string(request)
                    return redirect('?'.join([redirect_url, url_parameter_string]) if url_parameter_string != '' else redirect_url)
                    
                # redirect to thanks page if no choice-specific redirect URL (with all GET parameters as-is to be processed by thanks page)
                return HttpResponseRedirect('%s?%s' % (reverse('consultations:thanks', kwargs = {'pk': consultation.pk}), request.GET.urlencode()))
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

# passes on the URL parameters to the donation page
@login_required
def thanks(request, pk):
    consultation = get_object_or_404(Consultation, pk = pk)
    url_parameter_string = consultation.url_parameter_string(request)
    if url_parameter_string != '':
        url_parameter_string = '?%s' % url_parameter_string
    return render(request, 'consultations/thanks.html', { 
        'consultation': consultation,
        'url_parameter_string': url_parameter_string })
    
    

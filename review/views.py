from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Track, Theme, Proposal
from django.db.models import Count
from review.forms import EditProposalForm, ProposalForm, DeleteProposalForm

@login_required
def index(request):
    return render(request, 'review/index.html', { 
        'tracks' : Track.objects.all().order_by('display_order') })

@login_required
def track(request, pk):
    track = get_object_or_404(Track, pk = pk)
    return render(request, 'review/track.html', { 
        'track' : track, 
        'themes': track.themes.order_by('display_order') })
    
@login_required
def theme(request, pk):
    theme = get_object_or_404(Theme, pk = pk)
    user_proposal = theme.proposals.filter(created_by = request.user).first()
    return render(request, 'review/theme.html', { 
        'theme' : theme, 
        'proposals': theme.proposals.annotate(nomination_count = Count('nominations')).order_by('-nomination_count', 'created_at'),
        'user_proposal': user_proposal })

@login_required
def proposal(request, pk):
    # get the proposal
    proposal = get_object_or_404(Proposal, pk = pk)
    
    # increment the number of views only once per session
    session_key = 'viewed_proposal_{}'.format(pk)
    if not request.session.get(session_key, False):
        proposal.views += 1
        proposal.save()
        request.session[session_key] = True
        
    # render the form
    form = ProposalForm(instance = proposal)
    return render(request, 'review/proposal.html', { 
        'proposal' : proposal,
        'form': form })

@login_required
def new_proposal(request, pk):
    theme = get_object_or_404(Theme, pk = pk)
    if request.method == "POST":
        form = EditProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit = False)
            proposal.theme = theme
            proposal.created_by = request.user
            proposal.save()
            return redirect('review:proposal', pk = proposal.pk)
    else:
        form = EditProposalForm()
    return render(request, 'review/new_proposal.html', { 
        'theme' : theme,
        'form' : form })

@login_required
def edit_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk = pk)
    if proposal.created_by == request.user and request.method == "POST":
        form = EditProposalForm(request.POST, instance = proposal)
        if form.is_valid():
            proposal = form.save()
            return redirect('review:proposal', pk = proposal.pk)
    else:
        form = EditProposalForm(instance = proposal)
    return render(request, 'review/edit_proposal.html', { 
        'proposal' : proposal,
        'form' : form })

@login_required
def delete_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk = pk)
    if proposal.created_by == request.user and request.method == "POST":
        form = DeleteProposalForm(request.POST, instance = proposal)
        if form.is_valid():
            proposal.delete()
            return redirect('review:theme', pk = proposal.theme.pk)
    else:
        form = DeleteProposalForm(instance = proposal)
    return render(request, 'review/delete_proposal.html', { 
        'proposal' : proposal,
        'form' : form })

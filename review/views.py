from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Track, Theme, Proposal
from django.db.models import Count
from review.forms import NewProposalForm

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
    return render(request, 'review/theme.html', { 
        'theme' : theme, 
        'proposals': theme.proposals.annotate(nomination_count = Count('nominations')).order_by('-nomination_count', 'created_at') })

@login_required
def proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk = pk)
    proposal.views += 1
    proposal.save()
    return render(request, 'review/proposal.html', { 
        'proposal' : proposal })

@login_required
def new_proposal(request, pk):
    theme = get_object_or_404(Theme, pk = pk)
    if request.method == "POST":
        form = NewProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit = False)
            proposal.theme = theme
            proposal.created_by = request.user
            proposal.save()
            return redirect('review:proposal', pk = proposal.pk)
    else:
        form = NewProposalForm()
    return render(request, 'review/new_proposal.html', { 
        'theme' : theme,
        'form' : form })

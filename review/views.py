from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Track, Theme, Proposal
from django.db.models import Count

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
        'proposals': theme.proposals.annotate(nomination_count = Count('nominations')).order_by('-nomination_count') })

@login_required
def proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk = pk)
    return render(request, 'review/proposal.html', { 
        'proposal' : proposal })
    
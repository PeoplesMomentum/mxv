from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Track, Theme, Proposal, Amendment, Comment
from django.db.models import Count
from review.forms import EditProposalForm, ProposalForm, DeleteProposalForm, AmendmentForm, EditAmendmentForm, DeleteAmendmentForm, EditCommentForm, ModerationRequestForm, CommentForm

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
        'proposals': theme.proposals.annotate(nomination_count = Count('nominations')).order_by('-nomination_count', '-created_at'),
        'user_proposal': user_proposal })

@login_required
def proposal(request, pk):
    # get the proposal
    proposal = get_object_or_404(Proposal, pk = pk)

    # create the form for the proposal
    form = ProposalForm(instance = proposal)
    
    # if this is a post...
    if request.method == 'POST':
        
        # silent redirect back to proposal as the user must have crafted/cached a URL to get here
        if not proposal.theme.track.nominations_currently_allowed():
            return redirect('review:proposal', pk = proposal.pk)
        
        # if the form is valid...
        form = ProposalForm(request.POST)
        if form.is_valid():        
            
            # if nominating...
            if 'nominate' in request.POST:
                
                # clear existing user nominations in this theme
                for nomination in request.user.nominations.filter(proposal__theme = proposal.theme):
                    nomination.delete()
                
                # nominate the proposal
                proposal.nominations.create(proposal = proposal, nominated_by = request.user)
                
            # if clearing the nomination...
            if 'clear_nomination' in request.POST:
                
                # delete the nomination
                nomination = proposal.nominations.filter(nominated_by = request.user).first()
                if nomination:
                    nomination.delete()
                    
            return redirect('review:proposal', pk = proposal.pk)
    
    return render(request, 'review/proposal.html', { 
        'proposal' : proposal,
        'amendments' : proposal.amendments.order_by('-created_at'),
        'comments' : proposal.comments.order_by('-created_at'),
        'user_nominated': request.user.nominations.filter(proposal = proposal).exists(),
        'user_requested_moderation': request.user.moderation_requests.filter(proposal = proposal).first(),
        'form': form })

@login_required
def new_proposal(request, pk):
    theme = get_object_or_404(Theme, pk = pk)
    
    # silent redirect back to theme as the user must have crafted/cached a URL to get here
    if not theme.track.submissions_currently_allowed():
        return redirect('review:theme', pk = theme.pk)

    if request.method == "POST":
        form = EditProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit = False)
            proposal.theme = theme
            proposal.created_by = request.user
            proposal.save()
            return redirect('review:theme', pk = theme.pk)
    else:
        form = EditProposalForm()
    return render(request, 'review/new_proposal.html', { 
        'theme' : theme,
        'form' : form })

@login_required
def edit_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk = pk)
    
    # silent redirect back to proposal as the user must have crafted/cached a URL to get here
    if not proposal.theme.track.submissions_currently_allowed():
        return redirect('review:proposal', pk = proposal.pk)

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
    
    # silent redirect back to proposal as the user must have crafted/cached a URL to get here
    if not proposal.theme.track.submissions_currently_allowed():
        return redirect('review:proposal', pk = proposal.pk)

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

@login_required
def amendment(request, pk):
    amendment = get_object_or_404(Amendment, pk = pk)
    form = AmendmentForm(instance = amendment)
    return render(request, 'review/amendment.html', { 
        'amendment' : amendment,
        'user_requested_moderation': request.user.moderation_requests.filter(amendment = amendment).first(),
        'form': form })

@login_required
def new_amendment(request, pk):
    proposal = get_object_or_404(Proposal, pk = pk)
    
    # silent redirect back to proposal as the user must have crafted/cached a URL to get here
    if not proposal.theme.track.submissions_currently_allowed():
        return redirect('review:proposal', pk = proposal.pk)

    if request.method == "POST":
        form = EditAmendmentForm(request.POST)
        if form.is_valid():
            amendment = form.save(commit = False)
            amendment.proposal = proposal
            amendment.created_by = request.user
            amendment.save()
            return redirect('review:proposal', pk = proposal.pk)
    else:
        form = EditAmendmentForm()
    return render(request, 'review/new_amendment.html', { 
        'proposal' : proposal,
        'form' : form })

@login_required
def edit_amendment(request, pk):
    amendment = get_object_or_404(Amendment, pk = pk)
    
    # silent redirect back to proposal as the user must have crafted/cached a URL to get here
    if not amendment.proposal.theme.track.submissions_currently_allowed():
        return redirect('review:amendment', pk = amendment.pk)

    if amendment.created_by == request.user and request.method == "POST":
        form = EditAmendmentForm(request.POST, instance = amendment)
        if form.is_valid():
            amendment = form.save()
            return redirect('review:amendment', pk = amendment.pk)
    else:
        form = EditAmendmentForm(instance = amendment)
    return render(request, 'review/edit_amendment.html', { 
        'amendment' : amendment,
        'form' : form })

@login_required
def delete_amendment(request, pk):
    amendment = get_object_or_404(Amendment, pk = pk)
    
    # silent redirect back to proposal as the user must have crafted/cached a URL to get here
    if not amendment.proposal.theme.track.submissions_currently_allowed():
        return redirect('review:amendment', pk = amendment.pk)

    if amendment.created_by == request.user and request.method == "POST":
        form = DeleteAmendmentForm(request.POST, instance = amendment)
        if form.is_valid():
            amendment.delete()
            return redirect('review:proposal', pk = amendment.proposal.pk)
    else:
        form = DeleteAmendmentForm(instance = amendment)
    return render(request, 'review/delete_amendment.html', { 
        'amendment' : amendment,
        'form' : form })

@login_required
def new_comment(request, pk):
    proposal = get_object_or_404(Proposal, pk = pk)
    
    # silent redirect back to proposal as the user must have crafted/cached a URL to get here
    if not proposal.theme.track.allow_comments:
        return redirect('review:proposal', pk = proposal.pk)

    if request.method == "POST":
        form = EditCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.proposal = proposal
            comment.created_by = request.user
            comment.save()
            return redirect('review:proposal', pk = proposal.pk)
    else:
        form = EditCommentForm()
    return render(request, 'review/new_comment.html', { 
        'proposal' : proposal,
        'form' : form })

@login_required
def moderate_proposal(request, pk):
    # get the proposal
    proposal = get_object_or_404(Proposal, pk = pk)
        
    # if this is a valid post...
    if request.method == "POST":
        form = ModerationRequestForm('proposal', request.POST)
        if form.is_valid():
            
            # save the moderation request
            moderation_request = form.save(commit = False)
            moderation_request.proposal = proposal
            moderation_request.requested_by = request.user
            moderation_request.save()
            
            # notify that moderation is required
            moderation_request.notify_staff()
            
            # return to the referring entity
            return redirect("review:proposal", pk = pk)
    else:
        form = ModerationRequestForm('proposal')
    
    return render(request, 'review/moderate_proposal.html', {
        'proposal': proposal,
        'form' : form })
    
@login_required
def moderate_amendment(request, pk):
    # get the amendment
    amendment = get_object_or_404(Amendment, pk = pk)
        
    # if this is a valid post...
    if request.method == "POST":
        form = ModerationRequestForm('amendment', request.POST)
        if form.is_valid():
            
            # save the moderation request
            moderation_request = form.save(commit = False)
            moderation_request.amendment = amendment
            moderation_request.requested_by = request.user
            moderation_request.save()
            
            # notify that moderation is required
            moderation_request.notify_staff()
            
            # return to the referring entity
            return redirect("review:amendment", pk = pk)
    else:
        form = ModerationRequestForm('amendment')
    
    return render(request, 'review/moderate_amendment.html', {
        'amendment': amendment,
        'form' : form })
    
@login_required
def comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    form = CommentForm(instance = comment)
    return render(request, 'review/comment.html', { 
        'comment' : comment,
        'user_requested_moderation': request.user.moderation_requests.filter(comment = comment).first(),
        'form': form })

@login_required
def moderate_comment(request, pk):
    # get the comment
    comment = get_object_or_404(Comment, pk = pk)
        
    # if this is a valid post...
    if request.method == "POST":
        form = ModerationRequestForm('comment', request.POST)
        if form.is_valid():
            
            # save the moderation request
            moderation_request = form.save(commit = False)
            moderation_request.comment = comment
            moderation_request.requested_by = request.user
            moderation_request.save()
            
            # notify that moderation is required
            moderation_request.notify_staff()
            
            # return to the referring entity
            return redirect("review:comment", pk = pk)
    else:
        form = ModerationRequestForm('comment')
    
    return render(request, 'review/moderate_comment.html', {
        'comment': comment,
        'form' : form })
    

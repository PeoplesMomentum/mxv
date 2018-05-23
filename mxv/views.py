from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.views import PasswordResetView
from .settings import SITE_NAME_SHORT, SITE_NAME_LONG, ALLOW_ERROR_URL
from django.http import Http404
from mxv.settings import TRACK3_VOTING_VISIBLE_TO_NON_STAFF
from review.models import TrackVoting
from django.shortcuts import render, redirect
from mxv.models import Reconsent
from mxv.forms import ReconsentForm
from django.contrib import messages


# landing page
def index(request):
    template = loader.get_template('mxv/index.html')
    context = {
        'show_track3_voting': TRACK3_VOTING_VISIBLE_TO_NON_STAFF or request.user.is_staff,
        'track3_voting': TrackVoting.objects.filter(pk=3).first(),
    }
    return HttpResponse(template.render(context, request))

# pass the site names to the password reset context
class ExtraContextPasswordResetView(PasswordResetView):
    extra_email_context = {
         'site_name_short': SITE_NAME_SHORT,
         'site_name_long': SITE_NAME_LONG,
         }

# raises an error if allowed
def error(request):
    if ALLOW_ERROR_URL:
        raise Exception('error test')
    else:
        raise Http404('not found')
    
# returns the IP address from a request
def ip_from_request(request):
    
    # use the forwarded address if behind a router
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return(x_forwarded_for.split(',')[-1].strip())
    else:
        return(request.META.get('REMOTE_ADDR'))
        
# re-consent page
def reconsent(request):
    
    # if post...
    if request.method == 'POST':
        form = ReconsentForm(request.POST)
        
        # just complete if the re-consent already exists
        exists = Reconsent.objects.filter(email = form.data['email'])
        if exists:
            return redirect('reconsent_complete')
        
        # if valid post for new email...
        if form.is_valid():
            
            # save the email and IP
            reconsent = form.save(commit = False)
            reconsent.ip_address = ip_from_request(request)
            reconsent.save()
            
            # complete
            return redirect('reconsent_complete')
        
        else:
            #show errors
            messages.error(request, 'Please correct the errors below.')
            
    else:
        # check for an email parameter
        email = request.GET.get('email', None)
        
        if email:
            # set the email to be read-only if specified
            reconsent = Reconsent()
            reconsent.email = email
            form = ReconsentForm(instance = reconsent)
            form.fields['email'].widget.attrs['readonly'] = True
        else:
            form = ReconsentForm()
    
    return render(request, 'mxv/new_reconsent.html', { 
        'title' : 'Re-consent',
        'form' : form})
    
    
# re-consent complete page
def reconsent_complete(request):
    return render(request, 'mxv/reconsent_complete.html', { 
        'title' : 'Re-consent complete'})
    

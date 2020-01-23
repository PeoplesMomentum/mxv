from django.shortcuts import redirect, render
from voting_intentions.models import Vote, Intention
from mxv.settings import DEFAULT_REDIRECT_PAGE_URL

# records a voting intention from the URL parameters and redirects
def index(request):
        
    try:
        # get the vote if possible
        vote = None
        try:
            vote_id = request.GET.get('vote', None)
            vote = Vote.objects.filter(id = vote_id).first()
        except:
            pass
        
        # get the choice if possible
        choice = None
        try:
            choice_number = request.GET.get('choice', None)
            choice = vote.choices.filter(number = choice_number).first()
        except:
            pass
        
        # get the email
        email = request.GET.get('email', None)
        
        # record a voting intention if not already recorded
        if vote and choice and email:
            intention = Intention.objects.filter(vote = vote, choice = choice, email = email).first()
            if not intention:
                vote.intentions.create(vote = vote, choice = choice, email = email)
    
        # build the redirect
        redirect_url = choice.redirect_url if choice and choice.redirect_url != '' else vote.redirect_url if vote else DEFAULT_REDIRECT_PAGE_URL
        
        # build the URL parameters
        url_parameter_string = ''
        if vote:
            url_parameters_present = []
            for url_parameter in vote.url_parameters.all():
                if url_parameter.name in request.GET:
                    name = url_parameter.pass_on_name if url_parameter.pass_on_name else url_parameter.name
                    value = request.GET[url_parameter.name]
                    url_parameters_present.append((name, value))
            url_parameter_string = '&'.join('='.join(present) for present in url_parameters_present)
            
        # redirect
        return redirect('?'.join([redirect_url, url_parameter_string]) if url_parameter_string != '' else redirect_url)

    except Exception:
        return redirect(DEFAULT_REDIRECT_PAGE_URL)
   
# renders the thanks page 
def thanks(request):
    return render(request, 'voting_intentions/thanks.html')
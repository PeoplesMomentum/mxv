from django.shortcuts import redirect, render
from voting_intentions.models import Vote, Choice, Intention
from mxv.settings import DEFAULT_REDIRECT_PAGE_URL

# records a voting intention from the URL parameters and redirects
def index(request):
    
    try:
        # if the email, vote and intention are in the URL parameters...
        vote_id = request.GET.get('vote', None)
        choice_number = request.GET.get('choice', None)
        vote = Vote.objects.filter(id = vote_id).first()
        choice = vote.choices.filter(number = choice_number).first()
        email = request.GET.get('email', None)
        if vote and choice and email:
            
            # record a voting intention if not already recorded
            intention = Intention.objects.filter(vote = vote, choice = choice, email = email).first()
            if not intention:
                vote.intentions.create(vote = vote, choice = choice, email = email)
            
            # for each URL parameter that is present in the request...
            url_parameters_present = []
            for url_parameter in vote.url_parameters.all():
                if url_parameter.name in request.GET:
                    
                    # change its name if necessary and add it to the list of parameters present
                    name = url_parameter.name if url_parameter.pass_on_name == '' else url_parameter.pass_on_name
                    value = request.GET[url_parameter.name]
                    url_parameters_present.append((name, value))
                    
            # build the parameter string
            url_parameter_string = '&'.join('='.join(present) for present in url_parameters_present)
    
            # get the redirect URL (choice overrides vote if set)
            redirect_url = vote.redirect_url
            if choice.redirect_url != '':
                redirect_url = choice.redirect_url
    
            # redirect
            return redirect('?'.join([redirect_url, url_parameter_string]))
        
        else:
            # malformed request so just redirect to thanks/donation page
            if vote:
                return redirect(vote.redirect_url)
            else:
                return redirect(DEFAULT_REDIRECT_PAGE_URL)
    except Exception:
        return redirect(DEFAULT_REDIRECT_PAGE_URL)
   
# renders the thanks page 
def thanks(request):
    return render(request, 'voting_intentions/thanks.html')
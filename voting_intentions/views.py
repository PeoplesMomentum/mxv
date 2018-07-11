from django.shortcuts import get_object_or_404, redirect
from voting_intentions.models import Vote, Choice
from django.http.response import HttpResponseBadRequest

# records a voting intention from the URL parameters and redirects
def index(request):
    
    # if the email, vote and intention are in the URL parameters...
    vote = get_object_or_404(Vote, pk = request.GET['vote'])
    choice = get_object_or_404(Choice, pk = request.GET['choice'])
    email = request.GET['email']
    if email:
            
        # record a voting intention
        vote.intentions.create(vote = vote, choice = choice, email = email)
        
        # for each URL parameter that is present in the request...
        url_parameters_present = []
        for url_parameter in vote.url_parameters.all():
            if url_parameter.name in request.GET:
                
                # change its name if necessary
                name = url_parameter.name if url_parameter.pass_on_name == '' else url_parameter.pass_on_name
                value = request.GET[url_parameter.name]
                url_parameters_present.append((name, value))
                
        # pass the parameters on
        url_parameter_string = '&'.join('='.join(present) for present in url_parameters_present)

        # redirect
        return redirect('?'.join([vote.redirect_url, url_parameter_string]))
    
    else:
        return HttpResponseBadRequest()

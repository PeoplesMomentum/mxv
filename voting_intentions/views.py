from django.shortcuts import redirect
from voting_intentions.models import Vote, Choice
from mxv.nation_builder import NationBuilder
from mxv.settings import DEFAULT_REDIRECT_PAGE_URL

# records a voting intention from the URL parameters and redirects
def index(request):
    
    try:
        # if the email, vote and intention are in the URL parameters...
        vote_id = request.GET.get('vote', None)
        choice_id = request.GET.get('choice', None)
        vote = Vote.objects.filter(id = vote_id).first()
        choice = Choice.objects.filter(id = choice_id).first()
        email = request.GET.get('email', None)
        if vote and choice and email:
            
            # get the NB id for the email    
            nb = NationBuilder()
            nb_id = nb.IdFromEmail(email)
    
            # record a voting intention
            vote.intentions.create(vote = vote, choice = choice, email = email, nation_builder_id = nb_id)
            
            # set the vote and choice tags
            if nb_id:        
                # add tags
                add_tags = vote.vote_tags.filter(add=True).union(choice.choice_tags.filter(add=True))
                nb.SetPersonTags(nb_id, [tag.text for tag in add_tags])
                
                # remove tags
                remove_tags = vote.vote_tags.filter(add=False).union(choice.choice_tags.filter(add=False))
                nb.ClearPersonTags(nb_id, [tag.text for tag in remove_tags])
            
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
            # malformed request so just redirect to thanks/donation page
            if vote:
                return redirect(vote.redirect_url)
            else:
                return redirect(DEFAULT_REDIRECT_PAGE_URL)
    except:
        return redirect(DEFAULT_REDIRECT_PAGE_URL)
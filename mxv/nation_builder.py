import requests
from mxv.settings import NATIONBUILDER_API_TOKEN
from django.utils.http import urlencode

# encapsulates communications with the NationBuilder API
class NationBuilder:
    
    # the URL for people
    PERSON_URL = "https://momentum.nationbuilder.com/api/v1/people/%d?access_token=%s"
    MATCH_URL = "https://momentum.nationbuilder.com/api/v1/people/match?%s&access_token=%s"
    TAG_URL = "https://momentum.nationbuilder.com/api/v1/people/%d/taggings?access_token=%s"
    
    # whether to raise exceptions for HTTP status errors (not by default)
    raise_HTTP_errors = False
    def raise_for_status(self, response):
        if self.raise_HTTP_errors:
            response.raise_for_status()
    
    # returns a dictionary of field values for a person
    def GetPersonFields(self, person_id, field_names):
        
        # get the person's NB record
        response = requests.get(self.PERSON_URL % (person_id, NATIONBUILDER_API_TOKEN), timeout = 5)
        self.raise_for_status(response)
        record = response.json()
        
        # return the requested fields if the person was found
        if response.status_code == 200:
            return({ field_name: record['person'][field_name] for field_name in field_names })
        else:
            return None
    
    # sets the field values for a person
    def SetPersonFields(self, person_id, fields):
        
        # update the person's NB record
        response = requests.put(self.PERSON_URL % (person_id, NATIONBUILDER_API_TOKEN), json = { 'person':  fields }, timeout = 5)
        self.raise_for_status(response)

    # sets the tags for a person
    def SetPersonTags(self, person_id, tags):
        
        # set the tags
        response = requests.put(self.TAG_URL % (person_id, NATIONBUILDER_API_TOKEN), json = { 'tagging':  { 'tag': tags} }, timeout = 5)
        self.raise_for_status(response)

    # returns the NB id for an email
    def IdFromEmail(self, email):

        # get the matching NB record
        response = requests.get(self.MATCH_URL % (urlencode({ 'email': email }), NATIONBUILDER_API_TOKEN), timeout = 5)
        self.raise_for_status(response)
        record = response.json()
        
        # return the requested fields if the person was found
        if response.status_code == 200:
            return(record['person']['id'])
        else:
            return None

import requests
from mxv.settings import NATIONBUILDER_API_TOKEN
from django.utils.http import urlencode
from json_flatten import flatten, unflatten

# the NationBuilder API is slow enough that the rate limit shouldn't be hit from a single thread as shown by this experiment:
# 
# for i in range(1, 1000):
#     response = requests.head('https://momentum.nationbuilder.com/api/v1/sites?limit=1&access_token=[redacted]')
#     response.headers['X-RateLimit-Remaining']
#
# the lowest rate limit remaining value seen was 77 or thereabouts

# encapsulates communications with the NationBuilder API
class NationBuilder:
    
    # the API URLs
    PERSON_URL = "https://momentum.nationbuilder.com/api/v1/people/%d?access_token=%s"
    MATCH_URL = "https://momentum.nationbuilder.com/api/v1/people/match?%s&access_token=%s"
    TAG_URL = "https://momentum.nationbuilder.com/api/v1/people/%d/taggings?access_token=%s"
    
    # whether to raise exceptions for HTTP status errors (not by default)
    _raise_HTTP_errors = False
    
    # rate limit
    rate_limit_remaining = None
    
    # how long to wait in seconds for connect/read from NationBuilder
    default_timeout = 10
    
    # true if the rate limit has not been hit or is unknown
    def api_calls_available(self, required):
        return not self.rate_limit_remaining or self.rate_limit_remaining >= required
    
    # pulls rate limit headers from the response and raises status exceptions if configured to do so
    def _process_response(self, response):
        
        # rate limit headers
        self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', None))
    
        # status exceptions    
        if self._raise_HTTP_errors:
            response.raise_for_status()
            
    # returns a flattened list of (field_path = value) tuples for the person
    def PersonFieldsAndValues(self, person_id):
        
        # get the person's NB record
        response = requests.get(self.PERSON_URL % (person_id, NATIONBUILDER_API_TOKEN), timeout = self.default_timeout)
        self._process_response(response)
        
        # return field_path = value if the person was found
        if response.status_code == 200:
            record = response.json()
            flat = flatten(record)
            flat_list = []
            for key, value in flat.items():
                key_without_type = key if key.find('$') == -1 else key[:key.find('$')]
                value_without_none = value if value != 'None' else ''
                flat_list.append((key_without_type, value_without_none, "%s = %s" % (key_without_type, value_without_none)))
            flat_list.sort(key = lambda tup: tup[0])
            return(flat_list)
        else:
            return None
        
    # writes the values back to nation builder
    def SetFieldPathValues(self, person_id, field_path_values):
        
        # build record
        record = unflatten(field_path_values) 
        
        # write to nation builder
        response = requests.put(self.PERSON_URL % (person_id, NATIONBUILDER_API_TOKEN), json = record, timeout = self.default_timeout)
        self._process_response(response)    
        
    # returns a dictionary of field values for a person
    def GetPersonFields(self, person_id, field_names):
        
        # get the person's NB record
        response = requests.get(self.PERSON_URL % (person_id, NATIONBUILDER_API_TOKEN), timeout = self.default_timeout)
        self._process_response(response)
        
        # return the requested fields if the person was found
        if response.status_code == 200:
            record = response.json()
            return({ field_name: record['person'][field_name] for field_name in field_names })
        else:
            return None
    
    # sets the field values for a person
    def SetPersonFields(self, person_id, fields):
        response = requests.put(self.PERSON_URL % (person_id, NATIONBUILDER_API_TOKEN), json = { 'person':  fields }, timeout = self.default_timeout)
        self._process_response(response)

    # get the tags for a person
    def GetPersonTags(self, person_id):
        response = requests.get(self.TAG_URL % (person_id, NATIONBUILDER_API_TOKEN), timeout = self.default_timeout)
        self._process_response(response)
        
        # return the person's tags if the person was found
        if response.status_code == 200:
            record = response.json()
            return [tag['tag'] for tag in record['taggings']]
        else:
            return None

    # sets the tags for a person
    def SetPersonTags(self, person_id, tags):
        response = requests.put(self.TAG_URL % (person_id, NATIONBUILDER_API_TOKEN), json = { 'tagging':  { 'tag': tags} }, timeout = self.default_timeout)
        self._process_response(response)

    # clears the tags for a person
    def ClearPersonTags(self, person_id, tags):
        response = requests.delete(self.TAG_URL % (person_id, NATIONBUILDER_API_TOKEN), json = { 'tagging':  { 'tag': tags} }, timeout = self.default_timeout)
        self._process_response(response)

    # returns the NB id for an email
    def GetIdFromEmail(self, email):

        # get the matching NB record
        response = requests.get(self.MATCH_URL % (urlencode({ 'email': email }), NATIONBUILDER_API_TOKEN), timeout = self.default_timeout)
        self._process_response(response)
        
        # return the requested fields if the person was found
        if response.status_code == 200:
            record = response.json()
            return(record['person']['id'])
        else:
            return None

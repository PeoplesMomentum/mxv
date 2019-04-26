from .models import Task
from voting_intentions.models import Intention
from mxv.nation_builder import NationBuilder
from django.utils import timezone
from django.db import models

# these classes and their registrations in .admin should be moved to their related apps  
# difficult though because of TaskParentAdmin.child_models

# updates the voting intention tags in NationBuilder, respecting the NationBuilder API rate limit
class VotingIntentionTagTask(Task):
    
    maximum_attempts = models.IntegerField(default = 50)

    # updates the tags only if the rate limit has not been reached
    def execute(self, *args, **kwargs):

        # statistics
        attempted = 0
        successful = 0
        failed = 0
        rate_limit_hit = False
        done = False
        
        # while there are enough remaining executions (or the number of remaining executions is unknown)...
        nb = NationBuilder()
        while not done and not rate_limit_hit and attempted <= self.maximum_attempts and nb.api_calls_available(1):
            
            # and there are tags to update...
            intention = Intention.objects.filter(processed_at = None).first()
            if intention:
                
                # if this is the first access to NationBuilder and the rate limit is immediately hit then no id is returned but the email might still be known so abandon this run
                intention.nation_builder_id = nb.GetIdFromEmail(intention.email)
                rate_limit_hit = nb.rate_limit_remaining == 0
                if not rate_limit_hit:
                
                    # if the email is known to NationBuilder...
                    if intention.nation_builder_id:
                        
                        # and enough remaining executions...
                        if nb.api_calls_available(2):   
                             
                            # add tags
                            add_tags = intention.vote.vote_tags.filter(add=True).union(intention.choice.choice_tags.filter(add=True))
                            if len(add_tags) > 0:
                                nb.SetPersonTags(intention.nation_builder_id, [tag.text for tag in add_tags])
                            
                            # remove tags
                            remove_tags = intention.vote.vote_tags.filter(add=False).union(intention.choice.choice_tags.filter(add=False))
                            if len(remove_tags) > 0:
                                nb.ClearPersonTags(intention.nation_builder_id, [tag.text for tag in remove_tags])                
            
                            # record that any tags were written and don't process again
                            intention.tags_written_to_nation_builder = True
                            intention.email_unknown_in_nation_builder = False
                            intention.processed_at = timezone.now()
                            intention.save()
                            successful += 1
                        else:
                            # rate limit reached so process again
                            rate_limit_hit = True
                    else:
                        # record that the email was unknown and don't process again
                        intention.tags_written_to_nation_builder = False
                        intention.email_unknown_in_nation_builder = True
                        intention.processed_at = timezone.now()
                        intention.save()
                        failed += 1
                    
                attempted += 1
                    
            else:
                done = True
                
        return "Attempted: %d, successful: %d, failed: %d%s%s%s" % (
            attempted, 
            successful, 
            failed, 
            ", rate limit hit" if rate_limit_hit else "", 
            ", nothing more to do" if done else "",
            ", maximum attempts reached" if attempted == self.maximum_attempts else "")
            
# sends an email
class SendEmailTask(Task):
    def execute(self, *args, **kwargs):
        pass

# raises an exception
class RaiseExceptionTask(Task):
    def execute(self, *args, **kwargs):
        raise Exception('Raised from RaiseExceptionTask')

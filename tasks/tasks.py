from .models import Task
from voting_intentions.models import Intention
from mxv.nation_builder import NationBuilder

# should these classes and their registrations in .admin be moved to their related apps?  difficult because of TaskParentAdmin.child_models

# updates the voting intention tags in NationBuilder, respecting the NationBuilder API rate limit
class VotingIntentionTagTask(Task):
    
    # updates the tags only if the rate limit has not been reached (or is unknown)
    def execute(self, *args, **kwargs):
        
        intentions_processed = 0
        
        # while there are tags to update and remaining executions...
        nb = NationBuilder()
        done = False
        while not done and nb.api_calls_available(1):
            
            # if there are tags to update...
            intention = Intention.objects.filter(tags_written_to_nation_builder = False).first()
            if intention:
                
                # get the NB id for the email
                nb_id = nb.IdFromEmail(intention.email)
        
                # set the vote and choice tags
                if nb_id:
                    
                    if nb.api_calls_available(2):   
                         
                        # add tags
                        add_tags = intention.vote.vote_tags.filter(add=True).union(intention.choice.choice_tags.filter(add=True))
                        if len(add_tags) > 0:
                            nb.SetPersonTags(nb_id, [tag.text for tag in add_tags])
                        
                        # remove tags
                        remove_tags = intention.vote.vote_tags.filter(add=False).union(intention.choice.choice_tags.filter(add=False))
                        if len(remove_tags) > 0:
                            nb.ClearPersonTags(nb_id, [tag.text for tag in remove_tags])                
        
                        # record the update
                        intention.nation_builder_id = nb_id
                        intention.tags_written_to_nation_builder = True
                        intention.save()
                        intentions_processed += 1
                else:
                    # record that the email was unknown and don't process again
                    intention.email_unknown_in_nation_builder = True
                    intention.tags_written_to_nation_builder = True
                    intention.save()
                    intentions_processed += 1
                    
            else:
                done = True
                
        return "%d intention%s processed" % (intentions_processed, "s" if intentions_processed != 1 else "")
            
# sends an email
class SendEmailTask(Task):
    def execute(self, *args, **kwargs):
        pass

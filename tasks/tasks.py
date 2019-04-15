from .models import Task

# should these classes and their registrations in .admin be moved to their related apps?

# updates the voting intention tags in NationBuilder
class VotingIntentionTagTask(Task):
    pass

# sends an email
class SendEmailTask(Task):
    pass
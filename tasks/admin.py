from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from tasks.models import Task
from .tasks import VotingIntentionTagTask, SendEmailTask

@admin.register(Task)
class TaskParentAdmin(PolymorphicParentModelAdmin):
    base_model = Task
    child_models = (VotingIntentionTagTask, SendEmailTask)

class TaskChildAdmin(PolymorphicChildModelAdmin):
    base_model = Task
    readonly_fields = ('job_id', )

@admin.register(VotingIntentionTagTask)
class VotingIntentionTagTaskAdmin(TaskChildAdmin):
    base_model = VotingIntentionTagTask

    
@admin.register(SendEmailTask)
class SendEmailTaskAdmin(TaskChildAdmin):
    base_model = SendEmailTask

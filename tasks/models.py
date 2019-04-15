from django.db import models
from polymorphic.models import PolymorphicModel
import django_rq
from datetime import datetime

# an asynchronous task
class Task(PolymorphicModel):
    name = models.CharField(max_length = 100)
    start = models.DateTimeField(blank = True, null = True, default = None)
    repeat_seconds = models.IntegerField(blank = True, null = True, default = None)
    repeat_count = models.IntegerField(blank = True, null = True, default = None)
    enabled = models.BooleanField(default = True)
    job_id = models.CharField(max_length = 100, blank = True, null = True, default = None)
    
    def __str__(self):
        return self.name
        
    # override to provide the task's behaviour and return a result string
    def execute(self):
        return ''
    
    # override to provide arguments to execute
    def arguments(self):
        return []
    
    # runs the task if enabled and records the results of the run and any errors
    def run(self):
        if self.enabled:
            run = Run.objects.create(task = self)
            try:
                run.result = self.execute()
            except Exception as ex:
                Error.objects.create(run = run, error = ex.message)
            run.finish = datetime.utcnow()
            run.save()
        
    # (re)enqueues the task and saves the job id
    def save(self, *args, **kwargs):
        if self.job_id:
            django_rq.get_scheduler('default').cancel(self.job_id)
        job = None
        if not self.repeat_seconds:
            if not self.start:
                # run as soon as possible
                job = django_rq.enqueue(func = self.run, 
                                        args = self.arguments())
            else:
                # run when requested
                job = django_rq.get_scheduler('default').enqueue_at(scheduled_time = self.start, 
                                              func = self.run, 
                                              args = self.arguments())
        else:
            # run when and as often as requested
            job = django_rq.get_scheduler('default').schedule(scheduled_time = self.start if self.start else datetime.utcnow(), 
                                          func = self.run, 
                                          args = self.arguments(), 
                                          interval = self.repeat_seconds, 
                                          repeat = self.repeat_count)
        self.job_id = job.id
        super().save(*args, **kwargs)

    # removes the task's job from the queue
    def delete(self, *args, **kwargs):
        self.scheduler().cancel(self.job_id)
        super().delete(*args, **kwargs)

# a run of a task
class Run(models.Model):
    task = models.ForeignKey(Task, related_name='runs')
    start = models.DateTimeField(auto_now_add = True)
    finish = models.DateTimeField()
    result = models.TextField()
    
    def has_errors(self):
        return self.errors.count() > 0

# an error that occurred on a run
class Error(models.Model):
    run = models.ForeignKey(Run, related_name='errors')
    occurred_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField()


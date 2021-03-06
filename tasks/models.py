from django.db import models
from polymorphic.models import PolymorphicModel
import django_rq
from django.utils import timezone
import traceback
from django.db.models.deletion import CASCADE

# an asynchronous task
class Task(PolymorphicModel):
    name = models.CharField(max_length = 100)
    start = models.DateTimeField(blank = True, null = True, default = None, help_text = 'Time of first run (leave blank to run immediately)')
    repeat_seconds = models.IntegerField(blank = True, null = True, default = None, help_text = 'How often to repeat in seconds (leave blank to run only once)')
    repeat_count = models.IntegerField(blank = True, null = True, default = None, help_text = 'How many times to repeat (leave blank for indefinitely)')
    enabled = models.BooleanField(default = True)
    job_id = models.CharField(max_length = 100, blank = True, null = True, default = None)
    
    def __str__(self):
        return self.name
        
    # override to provide the task's behaviour and return a result string
    def execute(self, *args, **kwargs):
        pass
    
    # override to provide arguments to execute
    def arguments(self):
        pass
    
    # runs the task if enabled and records the results of the run and any errors
    def run(self, *args, **kwargs):
        if self.enabled:
            run = Run.objects.create(task = self)
            try:
                run.result = self.execute(*args, **kwargs)
            except:
                Error.objects.create(run = run, error = traceback.format_exc())
                run.result = 'Error'
            run.finish = timezone.now()
            run.save()
        
    # (re)enqueues the task and saves the job id
    def save(self, *args, **kwargs):
        # save immediately so that the task is available to any job that runs immediately
        super(Task, self).save(*args, **kwargs)
        
        # cancel existing job
        if self.job_id:
            django_rq.get_scheduler('default').cancel(self.job_id)
            self.job_id = None
            super(Task, self).save(*args, **kwargs)
            
        # create new job
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
            job = django_rq.get_scheduler('default').schedule(scheduled_time = self.start if self.start else timezone.now(), 
                                          func = self.run, 
                                          args = self.arguments(), 
                                          interval = self.repeat_seconds, 
                                          repeat = self.repeat_count)
        
        # save job id
        if job:
            self.job_id = job.id
            super(Task, self).save(*args, **kwargs)

    # removes the task's job from the queue
    def delete(self, *args, **kwargs):
        if self.job_id:
            django_rq.get_scheduler('default').cancel(self.job_id)
        super(Task, self).delete(*args, **kwargs)

# a run of a task
class Run(models.Model):
    task = models.ForeignKey(Task, related_name='runs', on_delete=CASCADE)
    start = models.DateTimeField(auto_now_add = True)
    finish = models.DateTimeField(blank = True, null = True, default = None)
    result = models.TextField(blank = True, null = True, default = None)

# an error that occurred on a run
class Error(models.Model):
    run = models.ForeignKey(Run, related_name='errors', on_delete=CASCADE)
    occurred_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField()


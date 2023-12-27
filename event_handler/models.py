from django.db import models
class PidHandlerModel(models.Model):
    class Meta:
        db_table = 'pid_handler'
    pid = models.TextField()
# Create your models here.
class EventHandlerModel(models.Model):
    class Meta:
        unique_together = ['event_name', 'queue_addr']
        db_table = 'event_handler'
    event_name = models.TextField()
    pid = models.TextField()
    status = models.TextField()
    progress = models.IntegerField()    
    queue_addr = models.TextField()
    update_time = models.DateTimeField(auto_now=True)
    
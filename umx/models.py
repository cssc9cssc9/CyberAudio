from django.db import models

# Create your models here.

class UMX(models.Model):
    file_path = models.TextField()
    model_dir = models.TextField()
    output_dir = models.TextField()
    do_separate_bass = models.BooleanField()
    do_separate_drums = models.BooleanField()
    do_separate_vocals = models.BooleanField()
    do_separate_other = models.BooleanField()
    
class Info(models.Model):
    queue_addr = models.IntegerField()
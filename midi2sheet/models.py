from django.db import models

class MidiToSheet(models.Model):
    base_dir = models.TextField()
# Create your models here.
class Merge(models.Model):
    melo_file = models.TextField()
    acco_file = models.TextField()
    output_file = models.TextField()

class Sheet(models.Model):
    tool_dir = models.TextField()
    input_file = models.TextField()
    output_dir = models.TextField()
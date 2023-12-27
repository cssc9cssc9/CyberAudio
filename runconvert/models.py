from django.db import models

# Create your models here.
class RunConvertModel(models.Model):
    input_music = models.TextField()
    output_midi = models.TextField()
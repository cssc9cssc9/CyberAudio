from django.db import models

# Create your models here.

class PresentIndex(models.Model):
    index_type = models.CharField(max_length=64)

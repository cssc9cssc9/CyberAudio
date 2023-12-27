from django.db import models

# Create your models here.

class CheckPidExistModel(models.Model):
    user_pid = models.TextField()
    class Meta:
        db_table = "check_pid_exist"
from django.db import models


# Create your models here.
class job_info(models.Model):
    name = models.CharField(max_length=30)
    job_kind = models.CharField(max_length=30)
    salary = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    jobtime = models.CharField(max_length=35)
    locate = models.CharField(max_length=35)
    information = models.CharField(max_length=100)

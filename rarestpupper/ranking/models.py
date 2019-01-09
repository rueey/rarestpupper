from django.db import models

# Create your models here.

class Pupper(models.Model):
    species = models.CharField(max_length=250)
    score = models.IntegerField(default=0)
    aggregate_score = models.IntegerField(default=0)
    update_time = models.DateTimeField('time updated')

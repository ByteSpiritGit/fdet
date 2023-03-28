from django.db import models

# Create your models here.
class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    claim = models.CharField(max_length=1000)
    label = models.CharField(max_length=100)
    supports = models.FloatField()
    refutes = models.FloatField()
    evidence = models.CharField(max_length=1000)
    def __str__(self):
        return self.claim
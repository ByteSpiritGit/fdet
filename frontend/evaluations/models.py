from django.db import models

# Create your models here.

class Evaluation_block(models.Model):
    id = models.AutoField(primary_key=True)
    # user_id = models.ForeignKey(to, on_delete)

    claims = models.TextField(null=True)

    def __str__(self):
        return str(self.id)

class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    evaluation_block = models.ForeignKey("Evaluation_block", on_delete=models.CASCADE)

    claim = models.CharField(max_length=1000)
    label = models.CharField(max_length=100)
    supports = models.FloatField(null=True)
    refutes = models.FloatField(null=True)
    ei = models.FloatField(null=True)
    nei = models.FloatField(null=True)
    evidence = models.TextField(null=True)
    justify = models.TextField(null=True)

    def __str__(self):
        return self.claim
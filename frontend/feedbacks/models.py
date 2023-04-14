from django.db import models
from evaluations.models import Evaluation_block, Evaluation

# Create your models here.
class Evaluation_Feedback(models.Model):
    id = models.AutoField(primary_key=True)

    feedback = models.BooleanField()
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)	

    def __str__(self):
        return str(self.id)

# class User_Feedback(models.Model):
#     id = models.AutoField(primary_key=True)
#     feedback = models.TextField()
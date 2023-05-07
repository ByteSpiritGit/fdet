from django.db import models
from evaluations.models import Evaluation_block, Evaluation
from django.contrib.auth.models import User

# Create your models here.
class Evaluation_Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    feedback = models.BooleanField()
    evaluation = models.ForeignKey(Evaluation_block, on_delete=models.CASCADE)	

    def __str__(self):
        return str(self.id)

class User_Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return str(self.id)
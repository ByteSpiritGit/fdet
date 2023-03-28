from django.db import models

# Create your models here.
class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    # evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)	
    feedback = models.TextField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
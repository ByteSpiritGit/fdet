from django.db import models

# !ALWAYS run makemigrations & migrate

# Create your models here.

class HomePage(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True) # blank - works with field, null - works with database
    summary = models.TextField()
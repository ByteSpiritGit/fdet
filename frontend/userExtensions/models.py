from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default_profile_picture.jpg', upload_to='./media/profile_pictures')
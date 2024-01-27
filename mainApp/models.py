from django.db import models

# Create your models here.

class BackgroundPicture(models.Model):
    pic = models.ImageField(upload_to='background_pic')
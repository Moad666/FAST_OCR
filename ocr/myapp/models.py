from django.db import models

# Create your models here.

class OCRResult(models.Model):
    image = models.ImageField(upload_to='images/')
    text = models.TextField()

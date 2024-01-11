from django.db import models

# Create your models here.

class OCRResult(models.Model):
    image = models.ImageField(upload_to='images/')
    text = models.TextField()

class OCRTask(models.Model):
    image = models.ImageField(upload_to='ocr_images/')
    result_text = models.TextField(blank=True)

class OCRTaskk(models.Model):
    image = models.ImageField(upload_to='ocr_images/')
    result_text = models.TextField(blank=True)
    array_date = models.TextField(blank=True)
    array_cin = models.TextField(blank=True)
    array_capital_word  = models.TextField(blank=True)
    def _str_(self):
        return f"OCRTask #{self.id}"

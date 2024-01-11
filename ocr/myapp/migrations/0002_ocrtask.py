# Generated by Django 4.1.7 on 2023-12-26 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OCRTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='ocr_images/')),
                ('result_text', models.TextField(blank=True)),
            ],
        ),
    ]

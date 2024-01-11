# Generated by Django 4.1.7 on 2024-01-11 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_ocrtask'),
    ]

    operations = [
        migrations.CreateModel(
            name='OCRTaskk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='ocr_images/')),
                ('result_text', models.TextField(blank=True)),
                ('array_date', models.TextField(blank=True)),
                ('array_cin', models.TextField(blank=True)),
                ('array_capital_word', models.TextField(blank=True)),
            ],
        ),
    ]
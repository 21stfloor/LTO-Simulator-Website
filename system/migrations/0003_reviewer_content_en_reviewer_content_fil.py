# Generated by Django 5.1 on 2024-08-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_question_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewer',
            name='content_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='reviewer',
            name='content_fil',
            field=models.TextField(null=True),
        ),
    ]
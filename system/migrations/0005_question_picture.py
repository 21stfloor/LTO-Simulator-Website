# Generated by Django 5.1 on 2024-08-20 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_reviewer_key_en_reviewer_key_fil'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='picture',
            field=models.ImageField(blank=True, default='', null=True, upload_to='images/questions/'),
        ),
    ]

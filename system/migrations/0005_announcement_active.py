# Generated by Django 4.1.5 on 2023-01-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_announcement_alter_score_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

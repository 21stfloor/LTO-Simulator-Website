# Generated by Django 4.2 on 2024-12-16 11:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_topuprecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='topuprecord',
            name='order_id',
            field=models.CharField(default=uuid.uuid4, max_length=255, unique=True),
        ),
    ]

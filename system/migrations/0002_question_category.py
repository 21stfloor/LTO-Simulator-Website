# Generated by Django 4.1.5 on 2024-07-10 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Traffic Rules and Regulations(Car)'), (1, 'Road Signage(Car)'), (2, 'Vehicle Basic Parts(Car)'), (3, 'Traffic Rules and Regulations(Motorcycle)'), (4, 'Road Signage(Motorcycle)'), (5, 'Vehicle Basic Parts(Motorcycle)')], default=0),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-06 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0005_numberofdays_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='berted_By',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='verted',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-06 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_numberofdays_leavespent'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberofdays',
            name='position',
            field=models.CharField(blank=True, choices=[('Junior Staff', 'Junior Staff'), ('Senior Staff', 'Senior Staff'), ('Director', 'Director')], max_length=100, null=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-06 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0006_leaverequest_berted_by_leaverequest_verted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaverequest',
            old_name='berted_By',
            new_name='verted_By',
        ),
    ]
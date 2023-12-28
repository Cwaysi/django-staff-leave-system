# Generated by Django 4.2.7 on 2023-12-06 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_customuser_firstname_customuser_surname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Numberofdays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(blank=True, choices=[('Annual Leave', 'Annual Leave'), ('Sick Leave', 'Sick Leave'), ('Study Leave', 'Study Leave'), ('Examination Leave', 'Examination Leave')], max_length=100, null=True)),
                ('days', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LeaveSpent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(blank=True, null=True)),
                ('leave_type', models.CharField(blank=True, choices=[('Annual Leave', 'Annual Leave'), ('Sick Leave', 'Sick Leave'), ('Study Leave', 'Study Leave'), ('Examination Leave', 'Examination Leave')], max_length=100, null=True)),
                ('days_spent', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
from django.contrib.auth.models import AbstractUser
from django.db import models

positionn = [
    ('Junior Staff', 'Junior Staff'),
    ('Senior Staff', 'Senior Staff'),
    ('Director', 'Director'),
]
dep = [
    ('ISD', 'ISD'),
    ('S&L', 'S&L'),
    ('RM&E', 'RM&E'),
    ('Administration', 'Administration'),
    ('Account', 'Account'),
    ('HR', 'HR'),
]
typ = [
    ('Annual Leave', 'Annual Leave'),
    ('Sick Leave', 'Sick Leave'),
    ('Study Leave', 'Study Leave'),
    ('Examination Leave', 'Examination Leave'),
]
stat =[
    ('Pending', 'Pending'),
      ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
]
class CustomUser(AbstractUser):
    firstname = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, blank=True, choices=positionn)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True, null=True, choices=dep)
    phone = models.CharField(max_length=15, blank=True)

class Holidays(models.Model):
    year = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    holiday = models.CharField(max_length=300, null = True, blank= True)

    def __str__(self):
        return self.holiday

class LeaveRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=typ)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.IntegerField(null = True, blank=True)
    verted = models.BooleanField(default=False)
    verted_By = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=stat, null = True, blank=True)
    relieving_Officer = models.CharField(max_length=50, null = True, blank=True)
    reason = models.TextField('Reasons for leave',null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    date_requested = models.DateField(auto_now_add=True)


class Numberofdays(models.Model):
    leave_type = models.CharField(max_length=100, null=True, blank=True, choices=typ)
    position = models.CharField(max_length=100, null=True, blank=True, choices=positionn)
    days = models.PositiveIntegerField()

    def __str__(self):
        return str(self.leave_type) + ' ' + str(self.position) +' - ' + str(self.days)

class LeaveSpent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    year = models.IntegerField(null=True, blank=True)
    leave_type = models.CharField(max_length=100, null =True, blank=True, choices=typ)
    days_spent = models.PositiveIntegerField()


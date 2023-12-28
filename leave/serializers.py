# serializers.py
from rest_framework import serializers
from .models import LeaveSpent

class LeaveSpentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveSpent
        fields = '__all__'

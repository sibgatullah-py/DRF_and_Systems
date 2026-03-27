from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
            "team",
        ]
        extra_kwargs = {
            "password":{"write_only":True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password) # Hashes the password instead of plain text
        user.save()
        return user
    
    
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
        
        
class WorkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLog
        fields = "__all__"
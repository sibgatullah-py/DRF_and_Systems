from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICE = (
        ("BOSS", "Boss"),
        ("LEADER", "Leader"),
        ("MEMBER", "Member"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICE)
    team = models.ForeignKey("Team", on_delete=models.SET_NULL, null=True, blank = True)
    # putting Team in "Team" is called lazy reference . Its used when Team model is defined later or in another app


class Team(models.Model):
    teamName = models.CharField(max_length=200)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    date = models.DateField()
    sign_in = models.DateTimeField()
    sign_out = models.DateTimeField(null=True, blank=True)
    
    active_hours = models.DurationField(null=True, blank=True)


class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    
    description = models.TextField()
    hours_spent = models.FloatField()
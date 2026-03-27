from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class User(AbstractUser):
    ROLE_CHOICE = (
        ("BOSS", "Boss"),
        ("LEADER", "Leader"),
        ("MEMBER", "Member"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICE)
    team = models.ForeignKey("Team", on_delete=models.SET_NULL, null=True, blank = True,related_name="members")
    # putting Team in "Team" is called lazy reference . Its used when Team model is defined later or in another app
    
    def __str__(self):
        return self.username


class Team(models.Model):
    teamName = models.CharField(max_length=200)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="leading_team")
    
    def save(self, *args, **kwargs):
        if self.leader and self.leader.role != "LEADER":
            raise ValidationError("Leader must have role LEADER")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.teamName


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
    
    date = models.DateField(auto_now_add=True)
    
    sign_in = models.DateTimeField()
    sign_out = models.DateTimeField(null=True, blank=True)
    
    active_hours = models.DurationField(null=True, blank=True)
    
    def save(self, *args,**kwargs):
        if self.sign_in and self.sign_out:
            self.active_hours = self.sign_out - self.sign_in
        super().save(*args,**kwargs)
        
    class Meta:
        unique_together = ['user','date']
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user} - {self.date}"


class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worklog')
    date = models.DateField(auto_now_add=True)
    
    description = models.TextField()
    hours_spent = models.FloatField(validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user} - {self.date}"
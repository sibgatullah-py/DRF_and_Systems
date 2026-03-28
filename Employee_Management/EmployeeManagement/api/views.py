from django.shortcuts import render

# <------------------------------------ Attendance starts(core) ----------------------------->
from rest_framework.views import APIView # APIView is used when i want to write custom logic 
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import *
from .permission import *
from .serializers import *

#SignIn API
class SignInView(APIView): # Custom end point for api(sign in)
    permission_classes = [IsMember] #Permission gate keeper(Members)
    
    def post(self,request): # User sends POST request for signing in here .
        user = request.user # After User sends the JWT token DRF checks the token and then sets request.user which is the logged in user
        today = timezone.now().date() # Get today's date
        
        #prevent duplicate (if there is already a sign in from this user then this will prevent another sign in )
        if Attendance.objects.filter(user=user, date=today).exists():
            return Response(
                {"error":"Already signed in today"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save sign-in time    
        Attendance.objects.create(
            user=user,
            sign_in=timezone.now()
        )
        
        return Response({"message":"Signed in successfully!"})# Response message if the whole method passes

    
#SignOut API
class SignOutView(APIView): #Custom endpoint for api(sign out)
    permission_classes = [IsMember] #Permission gatekeeper(Members)
    
    def post(self,request): #Taking post request which means the request will come as a form 
        user = request.user #Logged-in user
        today = timezone.now().date()
        
        attendance = Attendance.objects.filter(user=user, date=today).first() #Looking if the user already has signed in once
        
        if not attendance: #If not signed in
            return Response({"error":"Haven't signed in today"},
                            status=status.HTTP_400_BAD_REQUEST
                            )
            
        if attendance.sign_out: #If already signed out 
            return Response({"error":"Already signed out"},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        
        # This triggers active_hours = sign_out - sign_in    
        attendance.sign_out = timezone.now()
        attendance.save()
        
        return Response({"message":"Signed Out"})
    
# <--------------------------------------------- Attendance Ends(Core) ------------------------------------------------------------>


# <-------------------------------------------- Member Self Data APIs Starts ------------------------------------------------------>

#My Attendance
from rest_framework import generics

class MyAttendanceView(generics.ListAPIView): #Automatically returns a list
    serializer_class = AttendanceSerializer
    permission_classes = [IsMember] #Permission for only team members 
    
    def get_queryset(self): #Only show my(logged-in user) data
        return self.request.user.attendances.all()
    
#My Worklogs
class MyWorkLogView(generics.ListAPIView): #List of logged_in user's worklogs
    serializer_class = WorkLogSerializer
    permission_classes = [IsMember] #Permission for only team members
    
    def get_queryset(self): #Only return logged-in user's worklogs
        return self.request.user.worklogs.all()
    
#Create Worklogs 
class WorkLogCreateView(generics.CreateAPIView):
    serializer_class = WorkLogSerializer
    permission_classes = [IsMember]
    
    def perform_create(self, serializer): #This confirms the user is the logged in user preventing faking as other user
        serializer.save(user=self.request.user)
        
# <-------------------------------------------- Member Self Data APIs Ends ------------------------------------------------------>



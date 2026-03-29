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
        
# <-------------------------------------------- Member Self Data APIs Ends -------------------------------------------------------->


# <-------------------------------------------- LEADER VIEWS (TEAM ISOLATION) STARTS ---------------------------------------------->

#Team Members
class TeamMembersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsLeader]
    
    # this get_queryset method will fetch all users who are members of the same team as the logged-in user(leader)
    def get_queryset(self):
        return self.request.user.team.members.all() #Leader only sees his team his members

#Team Attendance
class TeamAttendanceView(generics.ListAPIView): #ListAPIView provides a read-only endpoint to list objects
    serializer_class = AttendanceSerializer
    permission_classes = [IsLeader]
    
    #user__team means: follow the user ForeignKey from Attendance to User, then the team ForeignKey from User to Team.
    def get_queryset(self): #Filters only this team
        return Attendance.objects.filter(
            user__team = self.request.user.team #user__team is called a double underscore lookup in Django ORM. IT's used to filter across model relationships
        )
        
#Team Worklog
class TeamWorkLogView(generics.ListAPIView):
    serializer_class = WorkLogSerializer
    permission_classes = [IsLeader]
    
    #user__team, this is called (Multi-tenant data isolation) *important concept 
    def get_queryset(self):
        return WorkLog.objects.filter(
            user__team = self.request.user.team
        )
    
        
# <-------------------------------------------- LEADER VIEWS (TEAM ISOLATION) ENDS ----------------------------------------------->


# <-------------------------------------------- BOSS VIEWS (FULL ACCESS) STARTS -------------------------------------------------->

#All Users
class AllUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsBoss]
    
#All Attendance
class AllAttendanceView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsBoss]
    
#All Worklogs 
class AllWorkLogView(generics.ListAPIView):
    queryset = WorkLog.objects.all()
    serializer_class = WorkLogSerializer
    permission_classes = [IsBoss]
    
# <-------------------------------------------- BOSS VIEWS (FULL ACCESS) ENDS ---------------------------------------------------->

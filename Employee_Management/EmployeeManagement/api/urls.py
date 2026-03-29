from django.urls import path
from .views import *

urlpatterns = [
    path("sign-in/", SignInView.as_view()),
    path("sign-out/", SignOutView.as_view()),

    path("my-attendance/", MyAttendanceView.as_view()),
    path("my-worklogs/", MyWorkLogView.as_view()),
    path("create-worklog/", WorkLogCreateView.as_view()),

    path("team-members/", TeamMembersView.as_view()),
    path("team-attendance/", TeamAttendanceView.as_view()),
    path("team-worklogs/", TeamWorkLogView.as_view()),
]

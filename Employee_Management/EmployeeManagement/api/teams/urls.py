from django.urls import path
from api.views import *

urlpatterns = [
    path('create/', CreateTeamView.as_view()),
    path('', TeamListView.as_view()),
    path('<int:team_id>/assign-leader/', AssignLeaderView.as_view()),
]
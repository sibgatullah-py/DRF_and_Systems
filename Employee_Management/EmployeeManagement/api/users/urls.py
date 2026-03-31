from django.urls import path
from api.views import *

urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('', AllUsersView.as_view()),
    path('<int:user_id>/assign-team/', AssignMemberView.as_view()),
]
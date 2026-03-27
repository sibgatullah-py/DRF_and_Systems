from django.shortcuts import render

# Attendance starts ----------------------------->
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Attendance
from .permission import IsMember


class SignInView(APIView):
    permission_classes = [IsMember]
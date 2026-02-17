from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .models import *
from .serializers import *

# for getting specific values according to id . django needs a queryset attribute or a get_queryset() method in viewset
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookSerializer(instance) 
        return Response(serializer.data)
    serializer_class = BookSerializer

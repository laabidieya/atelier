from django.shortcuts import render 
from rest_framework import viewsets
from Sessionapp.models import Session
from .serializers import SessionSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

from django.shortcuts import render
from .serializers import MessageSerializer
from .models import Message,Profile
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .import serializers
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RegisterProfileView(CreateAPIView):
    serializer_class = serializers.RegisterProfileSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room = self.kwargs['room_name']
        return Message.objects.filter(room_name=room).order_by('timestamp')
    
class RoomListView(generics.ListAPIView):
    serializer_class = serializers.RoomNameSerializer
    permission_classes = [IsAuthenticated]
    queryset=Message.objects.all()

    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = [serializers.CustomTokenObtainPairView]

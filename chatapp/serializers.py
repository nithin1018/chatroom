from .models import Message
from rest_framework import serializers
from rest_framework import serializers,status
from rest_framework.validators import ValidationError
from rest_framework.exceptions import ErrorDetail
from .models import Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class RoomNameSerializer(serializers.Serializer):
    room_name = serializers.CharField()

class RegisterProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password','confirm_password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists")
        return value
        

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError("Password doesnt match!")
        return attrs
    
    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        profile = Profile.objects.create(
            user=user
        )
        profile.bio = validated_data.get('bio', '')
        profile.save()

        return profile

class CustomTokenObtainPairView(TokenObtainPairView):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

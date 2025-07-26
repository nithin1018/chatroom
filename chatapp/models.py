from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(max_length=200, blank=True)
    profile_id = models.CharField(null=True,blank=True)

    def __str__(self):
        return f"{self.profile_id} -- {self.user.username}"
    
class Message(models.Model):
    room_name = models.CharField(max_length=100)
    user = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.room_name}] {self.user}: {self.content[:20]}"
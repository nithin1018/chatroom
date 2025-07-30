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
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="sent",default=1)
    reciever = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True,related_name="recieved")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.room_name}] {self.sender}: {self.content[:20]}"
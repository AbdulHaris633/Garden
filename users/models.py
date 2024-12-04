from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)  
    # country = models.CharField(max_length=100)
    name_privacy = models.BooleanField(default=True) 
    country_privacy = models.BooleanField(default=True)
    # region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='Users', null=True)
    
    def __str__(self):
        return self.username  

from django.db import models
from users.models import User
import uuid

class Post (models.Model):   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(max_length=100) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    

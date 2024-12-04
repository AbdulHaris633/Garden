
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=20)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name


class Region(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name  

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=15)
    image = models.CharField(max_length=255)
    days_to_maturity = models.CharField(max_length=20)
    mature_speed = models.CharField(max_length=20)
    mature_height = models.CharField(max_length=20)
    fruit_size = models.CharField(max_length=20)
    family = models.CharField(max_length=50) 
    type = models.CharField(max_length=50)
    native = models.CharField(max_length=50)
    hardiness = models.CharField(max_length=200)
    exposure = models.CharField(max_length=100)
    plant_dimension = models.CharField(max_length=50)
    variety_info = models.CharField(max_length=200)
    attributes = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    region = models.ManyToManyField(Region, related_name='region')
    

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)  
    # country = models.CharField(max_length=100)
    name_privacy = models.BooleanField(default=True) 
    country_privacy = models.BooleanField(default=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='Users', null=True)
    
    def __str__(self):
        return self.username


class Garden(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='garden_user')
    # products = models.ManyToManyField(Product, related_name='gardens_products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Garden owned by {self.user.username}"
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.CharField(max_length=255) 
    description = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
# use charField form image url and store it on amazonre s3 bucket
    
    

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=255) 
    article_link = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Article by {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    

class ChatBox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()  
    answer = models.TextField()  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Chat with {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    
class ReportAProblem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Images of {self.user.username}"


class GardenProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)  # Track when the product was added
    quantity = models.PositiveIntegerField(default=1)  # Optional: Track quantity
    # is_expose_sun = models.BooleanField(default=True)
    # expose_to_sun_date = models.DateTimeField(auto_now_add=True)  # Track when the product was added
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.garden.user.username}'s garden"

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    image = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_user')
    # how to implement multiples products for a user and keep track of it after add to a virtual garden
    garden_product = models.ForeignKey(GardenProduct, on_delete=models.CASCADE, related_name='notifications_garden_product') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=150,unique=True)
    phone_number=models.CharField(unique=True)
    occupation=models.CharField(max_length=150,blank=True)
    profile_picture=models.FileField(upload_to='profile_pics',blank=True)#upload_to='profile_pics',
    slug=models.SlugField(default="",null=False,unique=True,db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.username)
        super().save(*args,**kwargs)

    

class Post(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post_text=models.TextField()
    post_image=models.FileField(upload_to='post_picture',blank=True)
    uploaded_date=models.DateTimeField(auto_now_add=True)
    no_of_likes=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}-{self.uploaded_date}"
    

class Comment(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    

class Follow(models.Model):
    follower=models.ForeignKey(UserProfile,related_name="follower",on_delete=models.CASCADE)
    following=models.ForeignKey(UserProfile,related_name='following',on_delete=models.CASCADE)
    followed_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    

class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

#models for the crop information section 
class CropInfo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    varieties = models.TextField()
    climate_and_soil_requirements = models.TextField()
    planting_time = models.TextField()
    watering_needs = models.TextField()
    fertilization = models.TextField()
    pest_and_disease_management = models.TextField()
    harvesting_time = models.TextField()
    post_harvest_handling = models.TextField()
    market_information = models.TextField()
    government_schemes_and_subsidies = models.TextField()
    picture=models.FileField(upload_to='crop_pics',blank=True)
    def __str__(self):
        return self.name

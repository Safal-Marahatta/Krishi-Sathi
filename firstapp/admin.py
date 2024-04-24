from django.contrib import admin

# Register your models here.
from .models import UserProfile, Post, Comment, Follow,Like,CropInfo

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(CropInfo)
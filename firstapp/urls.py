from django.urls import path
from .  import views

urlpatterns=[
    path("",views.login_page,name="login"),# this will trigger domain/challenges/
    path("home/",views.home,name="homepage"),
    path("home/forum",views.forum,name="forumpage"),
    path("register/",views.register,name="register"),
    path("logout/",views.logout_page,name="logout"),
    path("home/forum/profile",views.my_profile,name="my_profile"),
    path("home/forum/search",views.search_people,name="search_people"),
    path("home/forum/<slug:slug>",views.individual_people,name="individual_people"),
    path("cropInfo/",views.cropInfo,name="cropInfo"),
    path("crop_detail/<str:name>",views.crop_detail,name="crop_detail"),
    path('predict/',views.predict_crop_portal, name='predict'),
    path('recommend/',views.recommend, name='recommend'),
    path("following_feed",views.following_feed,name="following_feed"),
    path("forum/fans",views.fans,name="fans")
]
#pg_ctl start -D "C:\Program Files\PostgreSQL\16\data"
from firstapp.views import load_more_posts,follow_controller,search_recommend_api,username_warning,phonenumber_warning,thulo_post_data,handle_vitri_follow,postComments,bahiri_like,get_profile_posts,predict_crop_disease,news_api_proxy,load_following_posts,handle_profile_follow

from django.urls import path

urlpatterns=[
    path('getposts/',load_more_posts),
    path('follow/',follow_controller),
    path('username_warning/',username_warning),
    path('search_people_suggestion/',search_recommend_api),
    path('phonenumber_warning/',phonenumber_warning),
    path('thulo_post_data/',thulo_post_data),
    path('handle_vitri_follow/',handle_vitri_follow),
    path('handle_profile_follow/',handle_profile_follow),
    path("postComments/",postComments),
    path("bahiri_like/",bahiri_like),
    path('get_profile_posts/',get_profile_posts),
    path('predict_diesease/',predict_crop_disease),
    path('news/', news_api_proxy, name='news_api_proxy'),
    path('following_posts/',load_following_posts),
]
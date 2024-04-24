from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
#from django.urls import reverse
#from django.template.loader import render_to_string
#from django.contrib.auth.hashers import make_password, check_password
from .forms import loginform,user_post,RegistrationForm,CropPredictionForm
from .models import UserProfile,Post,Follow,Comment,Like,CropInfo
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PostSerializer,UserProfileSerializer,CommentSerializer

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.models import load_model
import os
from django.conf import settings

#concept:           1.Django comes with a built-in user model called User. This model includes fields like username, password, and email. It also comes with features like password hashing and authentication methods.
modelstraw=load_model("F:/vs code/farmer/latest_models/strawberry.h5")
modelcorn=load_model("F:/vs code/farmer/latest_models/corn_latest.h5")
modelgrape=load_model('F:/vs code/farmer/latest_models/grape _latest.h5')
modelapple=load_model('F:/vs code/farmer/latest_models/apple.h5')
modelpotato=load_model('F:/vs code/farmer/latest_models/potato.h5')


def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=form.cleaned_data['username']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            occupation=form.cleaned_data['occupation']
            uploaded_photo=request.FILES["profile_image"]
            
            # Save the file to the media directory using FileSystemStorage
            file_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', uploaded_photo.name)
            # Save the file to MEDIA_ROOT
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_photo.chunks():
                    destination.write(chunk)
        

            try:
                user = User.objects.create_user(username=username,email=email,password= password,first_name=first_name,last_name=last_name)#At this point, user is a User object that has already been saved to the database.
                #if you want to change other fields.
                    #>>> user.last_name = "Lennon"
                    #>>> user.save()
            
                    ##########Also creating a User Profile  
                user_prof_obj=UserProfile(user=user,username=username,phone_number=phone_number,occupation=occupation,profile_picture=file_path )
                user_prof_obj.save()
                return redirect('login')#Redirect to the login page after sucessful registration
            except:
                return HttpResponse('An error occurred while creating the user profile')
    
    
    else:
        logout(request)
        form=RegistrationForm()
    

    return render(request,"firstapp/register_page.html",{'form':form})





def login_page(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            print('valid form')
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username,password=password)#If the credentials are valid, the function returns a user object representing the authenticated user. 
                                                                              #If the credentials are invalid, the function returns None.
            
           ## eg. this gives the username of the user:::print(user.get_username())
            
            if user is not None:
                login(request,user)#yesle k garxa vane:
#                            -->aauta session banaidinxa ani tesma session data haru store gardinxa.tyo session id chai cookie ko rup ma send gardinxa browser lai.
#                            -->aba tyo data haru request.session.get('_auth_user_id',default='default') yesto garera herna milxa.
                return redirect('homepage')
    else:
        form = loginform()
    return render(request, 'firstapp/login.html', {'form': form})





# def login(request):
#     if request.method=='POST':
#         form=loginform(request.POST)
#         if form.is_valid():
#             phno=form.cleaned_data['phone_number']
#             password=form.cleaned_data['password']

#             try:
#                 user=UserProfile.objects.get(phone_number=phno)
#                 if password==user.password:
#                      # Password is correct, perform login logic here (e.g., setting session variables)
#                     print("correct")
#                     request.session['logged_status']='1'
#                     request.session.set_expiry(0)
#                     return  HttpResponseRedirect('/home')
#                     #return  redirect('homepage')
#                 else:
#                     return render(request,'firstapp/login.html', {'form': form})

#             except:
#                 return render(request,'firstapp/login.html', {'form': form})
            
#     else:
#         form=loginform()
#         return render(request,'firstapp/login.html',{'form':form})





def logout_page(request):
    logout(request)
    return redirect('login')
#the things done by logout(request) are:
#     -->The user is marked as not authenticated. The request.user attribute will be set to an instance of AnonymousUser, indicating that no user is currently logged in.
#     -->The user's session data is cleared. Any data stored in the session for that particular user will be removed.
#     -->The session cookie, which is used to identify the user's session, is cleared. This cookie typically stores the session ID
#     -->If your application uses Django's CSRF protection, the CSRF token for the user is invalidated
#     -->Any other authentication-related cookies, if present, may also be cleared.




@login_required(login_url="/")#The @login_required decorator in Django is used to restrict access to a view so that only authenticated users can access it. If a user is not authenticated, the decorator will redirect them to the login page.
def home(request):
    return render(request, 'firstapp/home.html')




@login_required(login_url="/")
def forum(request):
    if request.method=='POST':
        form=user_post(request.POST,request.FILES)
        current_user=request.user#current_user ma chai user_object aayo
        post_garne_user=current_user.username
        print(post_garne_user)
        if form.is_valid():
            #save the form to database
            post_text=form.cleaned_data['post_text']
            post_image = form.cleaned_data['post_image']
            user_profile_instance=UserProfile.objects.get(username=post_garne_user)
            post=Post(post_image=post_image,post_text=post_text,user=user_profile_instance)
            post.save()
            return HttpResponseRedirect("/home/forum")
    elif request.method=='GET':
        form=user_post()
    ##########################################################################
    request.session["first"] = "3000"#note this is temporary. yeslai api call mai if halera assign garne
    request.session["second"] ="2000"
    request.session["third"] ="1500"

    ###########################################################################

    return render(request, 'firstapp/forum.html', {'form': form})

@login_required(login_url="/")
def cropInfo(request):
    return render(request,"firstapp/infoHome.html")

@login_required(login_url="/")
def my_profile(request):
    if request.method=="GET":
        current_user=request.user
        user_profile_instance=current_user.userprofile
        image_src=user_profile_instance.profile_picture
        print(image_src)
        print(user_profile_instance.username)#upto here it is correct aba profile picture pani capture garne form banayera profile picture store garnaparyo. ani tesko url chai tyo template ko src ma halera pathaidinu paryo.

        #for finding the total number of followers:
        follower_count=Follow.objects.filter(following=user_profile_instance).count()

        #for finding the number of following
        following_count=Follow.objects.filter(follower=user_profile_instance).count()

        message="EditProfile"
##########################################################################
        request.session["f"] = "3000"#note this is temporary. yeslai api call mai if halera assign garne
        request.session["s"] ="2000"
        request.session["t"] ="1500"

###########################################################################


        return render(request,"firstapp/profile.html",{"user_profile":user_profile_instance,"follower":follower_count,"following":following_count,"message":message})


@login_required(login_url="/")
def search_people(request):#search ma lekhera enter dabayesi
    if(request.method=="GET"):
        currentuser_profile_obj=UserProfile.objects.get(username=request.user.username)
        if "query" in request.GET:
            query=request.GET['query']
            try:
                user_profile_instance=UserProfile.objects.get(username__iexact=query)
                follower_count=Follow.objects.filter(following=user_profile_instance).count()
                following_count=Follow.objects.filter(follower=user_profile_instance).count()

                if currentuser_profile_obj.id == user_profile_instance.id:
                    message="EditProfile"
                else:
                    if Follow.objects.filter(follower=currentuser_profile_obj, following=user_profile_instance).exists():
                        message="UnFollow"
                    else:
                        message="Follow"
    #####################################################################################################################            
                request.session["f"] = "3000"#note this is temporary. yeslai api call mai if halera assign garne
                request.session["s"] ="2000"
                request.session["t"] ="1500"
    ########################################################################################################################            
                return render(request,"firstapp/profile.html",{"user_profile":user_profile_instance,"follower":follower_count,"following":following_count,"message":message})
            except ObjectDoesNotExist:
                #handling the case where no matching user profile is found
                return render(request,"firstapp/profile_error.html",{"error_message":"Profile not found"})
        else:
            return HttpResponse("AN ERROR OCCURED")
    

@login_required(login_url="/")
def individual_people(request,slug):
    if request.method=="GET":
        currentuser_profile_obj=UserProfile.objects.get(username=request.user.username)
        try:
            user_profile_instance=UserProfile.objects.get(slug=slug)
        except:
            return render(request,"firstapp/profile_error.html")
        follower_count=Follow.objects.filter(following=user_profile_instance).count()
        following_count=Follow.objects.filter(follower=user_profile_instance).count()

        if currentuser_profile_obj.id == user_profile_instance.id:
            message="EditProfile"
        else:
            if Follow.objects.filter(follower=currentuser_profile_obj, following=user_profile_instance).exists():
                message="UnFollow"
            else:
                message="Follow"
#####################################################################################################################            
        request.session["f"] = "3000"#note this is temporary. yeslai api call mai if halera assign garne
        request.session["s"] ="2000"
        request.session["t"] ="1500"
########################################################################################################################            
        return render(request,"firstapp/profile.html",{"user_profile":user_profile_instance,"follower":follower_count,"following":following_count,"message":message})        

    

@api_view(['GET'])
def load_more_posts(request):
    try:   
        currentuser_profile_obj=UserProfile.objects.get(username=request.user.username)# Assuming the user is logged in, get the UserProfile
        
        three_posts=[]
        print("before the loop")
        #yeta if pageno==1 garera tyo browser le deko page number check garera tyo session lai initialize garaune 
        #note tyo profile ma gayera back garda ali ghau vai raxa.
        latest_posts = Post.objects.order_by('-uploaded_date')

        for latest_post in latest_posts:
            if len(three_posts)<3:
                if int(latest_post.id)==int(request.session.get("first")) or int(latest_post.id)==int(request.session.get("second")) or int(latest_post.id)==int(request.session.get("third")):
                    print("paile ko ho yo")            
                elif int(latest_post.id)<int(request.session.get("third")):
                    three_posts.append(latest_post)
                elif int(latest_post.id)>int(request.session["first"]):
                    print("mathi nahi badega only tala")
            else:
                break

        print("after the loop")
        print(three_posts)

        follow_status=[]#yesma 3 ta element hunxa josle k vanxa vani yo current user chai tyo post ko author lai follow garya xa ki xaina
        for posts in three_posts:
            print("follow vitra")
            post_author_obj=posts.user
            is_following = Follow.objects.filter(follower=currentuser_profile_obj, following=post_author_obj).exists()
            if is_following:
                follow_status.append("unfollow")
            else:
                follow_status.append("follow")

        print("follow bahira")
        

        like_status=[]
        for posts in three_posts:
            has_like=Like.objects.filter(post=posts,user=currentuser_profile_obj).exists()
            if has_like:
                like_status.append("has_liked")
            else:
                like_status.append("has_not")
        
        comment_count=[]
        like_count=[]
        for posts in three_posts:
            c_count=Comment.objects.filter(post=posts).count()
            l_count=Like.objects.filter(post=posts).count()
            like_count.append(l_count)
            comment_count.append(c_count)
            


        if len(three_posts)==0:#or yesma tyo session lai reassign garera feri first batai data lina pani sakinxa
            print("the session is not changed. as it is was previous")
        if len(three_posts)==1:
            request.session["first"] = three_posts[0].id
            request.session["second"] = three_posts[0].id
            request.session["third"] =three_posts[0].id
        if len(three_posts)==2:
            request.session["first"] = three_posts[0].id
            request.session["second"] = three_posts[0].id
            request.session["third"] =three_posts[1].id 
        if len(three_posts)==3:
            request.session["first"] = three_posts[0].id
            request.session["second"] = three_posts[1].id
            request.session["third"] =three_posts[2].id                 


        print("assign garesi")
        print(request.session["first"])
        print(request.session["second"])
        print(request.session["third"])

        serializer=PostSerializer(three_posts,many=True)
        print('ok')
        return Response({'posts':serializer.data,'follow_status':follow_status,'like_status':like_status,"comment_count":comment_count,"like_count":like_count},status=200)
    except:
        return Response('sorry',status=500)        





@api_view(['POST','GET'])
def follow_controller(request):
    if (request.method=='POST'):
        #first checking wether the request is to follow or unfollow
        if(request.data['status']=='.Follow'):
            #print("follow garauna paryo")
            current_user=request.user
            follow_garne_user=current_user.username
            print(follow_garne_user)
            follow_garne_user_object= UserProfile.objects.get(username=follow_garne_user)
            try:
                post_wala_manxe=request.data['username']#follow hune manxe
                postwala_manxe_object=UserProfile.objects.get(username=post_wala_manxe)
                try:
                    Follow.objects.filter(follower=unfollow_garne_user_object, following=postwala_manxe_object).exists()
                except:
                    follow_object=Follow(follower=follow_garne_user_object,following=postwala_manxe_object)
                    follow_object.save()
                    print('added')
                    return Response("ok",status=200)

            except:
                return Response("error",status=404)

        else:
            #print("unfollow garauna paryo")
            current_user=request.user
            unfollow_garne_user=current_user.username
            print(unfollow_garne_user)
            unfollow_garne_user_object= UserProfile.objects.get(username=unfollow_garne_user)
            try:
                post_wala_manxe=request.data['username']#follow hune manxe
                print(post_wala_manxe)
                postwala_manxe_object=UserProfile.objects.get(username=post_wala_manxe)
                if (Follow.objects.filter(follower=unfollow_garne_user_object, following=postwala_manxe_object).exists()):
                    follow_object=Follow.objects.filter(follower=unfollow_garne_user_object,following=postwala_manxe_object)
                    follow_object.delete()
                    print('deleted')
                    return Response("ok",status=200)

            except:
                return Response("error",status=404)
    

@api_view(['GET'])
def search_recommend_api(request):#showing dynamic search results
    try:
        query=request.GET.get('query','')
        print(query)
        results=UserProfile.objects.filter(username__icontains=query)
        serializer=UserProfileSerializer(results,many=True)
        return Response(serializer.data,status=200)
    except:
        return Response("sorry",status=500)


@api_view(['GET'])
def username_warning(request):
    try:
        query=request.GET.get('query','')
        print(query)
        if UserProfile.objects.filter(username__iexact=query).exists():
            return Response({"message":"yes"})
        else:
            return Response({"message":"no"})
    except:
        return Response("some error",status=500)

@api_view(['GET'])
def phonenumber_warning(request):
    try:
        query=request.GET.get('query','')
        print(query)
        if UserProfile.objects.filter(phone_number__iexact=query).exists():
            return Response({"message":"yes"})
        else:
            return Response({"message":"no"})
    except:
        return Response("some error",status=500)
    

@api_view(['GET'])
def thulo_post_data(request):
    try:   
        currentuser_profile_obj=UserProfile.objects.get(username=request.user.username)# Assuming the user is logged in, get the UserProfile
    except:
        return Response('invalid_user',status=404)


    try:
        query=request.GET.get('query','')#post ko id
        print(query)
        response_data=Post.objects.get(id=str(query))#post object
    except:
        return Response("no_data",status=404)
    

    try:
        post_comments=Comment.objects.filter(post=response_data)
        commentserializer=CommentSerializer(post_comments,many=True)
    except:
        return Response("no_data",status=404)


    try:
        post_author_obj=response_data.user
        is_following = Follow.objects.filter(follower=currentuser_profile_obj, following=post_author_obj).exists()
        if is_following:
            follow_status=".Unfollow"
        else:
            follow_status=".Follow"

        is_liking= Like.objects.filter(post=response_data, user=currentuser_profile_obj).exists()
        if is_liking:
            like_status="liked"
        else:
            like_status="not_liked"

        
        total_likes = Like.objects.filter(post=response_data).count()
        total_comments = Comment.objects.filter(post=response_data).count()

        serializer=PostSerializer(response_data,many=False)
        combined_data={'data':serializer.data,'follow_status':follow_status,'comments':commentserializer.data,'like_status':like_status,'like_count':total_likes,'comment_counts':total_comments}
        return Response(combined_data,status=200)
    except:
        return Response("some_error",status=404)
    

@api_view(['post'])
def handle_vitri_follow(request):
    if request.method=="POST":
        post_id=request.data['post']
        current_user=request.user
        currentuser_profile_obj=UserProfile.objects.get(user=current_user)# Assuming the user is logged in, get the UserProfile
        print(current_user)
        follow_hune_manxe=Post.objects.get(id=post_id).user
        print(follow_hune_manxe)
        if Follow.objects.filter(follower=currentuser_profile_obj, following=follow_hune_manxe).exists():
            print("unfollow garauna paryo")
            follow_object=Follow.objects.filter(follower=currentuser_profile_obj,following=follow_hune_manxe)
            follow_object.delete()
            print('unfollowed')

        else:
            print("follow garauna paryo")
            follow_object=Follow(follower=currentuser_profile_obj,following=follow_hune_manxe)
            follow_object.save()

        return Response("testing",status=200)
    
@api_view(['post'])
def handle_profile_follow(request):
    if request.method=="POST":
        current_user=request.user
        currentuser_profile_obj=UserProfile.objects.get(user=current_user)# Assuming the user is logged in, get the UserProfile
        print(current_user)
        follow_hune_manxeid=request.data['profile']
        follow_hune_profobj=UserProfile.objects.get(id=follow_hune_manxeid)
        print(follow_hune_manxeid)
        if Follow.objects.filter(follower=currentuser_profile_obj, following=follow_hune_profobj).exists():
            print("unfollow garauna paryo")
            follow_object=Follow.objects.filter(follower=currentuser_profile_obj,following=follow_hune_profobj)
            follow_object.delete()
            print('unfollowed')

        else:
            print("follow garauna paryo")
            follow_object=Follow(follower=currentuser_profile_obj,following=follow_hune_profobj)
            follow_object.save()
        return Response("testing",status=200)  
    
@api_view(['POST'])
def postComments(request):
    if request.method=="POST":
        try:
            post_id=request.data['post']
            com_text=request.data['comment']
            current_user=request.user
            currentuser_profile_obj=UserProfile.objects.get(user=current_user)# Assuming the user is logged in, get the UserProfile
            post_obj=Post.objects.get(id=post_id)
            commentObject=Comment(user=currentuser_profile_obj,post=post_obj,comment_text=com_text)
            commentObject.save()
            total_comments = Comment.objects.filter(post=post_obj).count()
            return Response({"total_comments":total_comments},status=200)
        except:
            return Response('error',status=404)
    
@api_view(['POST'])
def bahiri_like(request):#note bahiri like ra vitri like lai control garna ko lagi same nai function use gareko xa hai
    if request.method=="POST":
        try:
            post_id=request.data['post']
            current_user=request.user
            currentuser_profile_obj=current_user.userprofile
            post_obj=Post.objects.get(id=post_id)
            if Like.objects.filter(post=post_obj,user=currentuser_profile_obj).exists():
                print("like hatauna paryo")
                like_object=Like.objects.filter(post=post_obj,user=currentuser_profile_obj)
                like_object.delete()
            else:
                print("like relation establish garauna paryo")
                like_object=Like(post=post_obj,user=currentuser_profile_obj)
                like_object.save()
            total_likes = Like.objects.filter(post=post_obj).count()

            return Response({"like":total_likes},status=200)
        except:
            return Response("some error",status=500)

#####################for the profile page################################
@api_view(['POST','GET'])
def get_profile_posts(request):
    try: 
        query_userid=request.GET.get('profileOf',None)  
        currentuser_profile_obj=UserProfile.objects.get(id=query_userid)# Assuming the user is logged in, get the UserProfile
        
        three_posts=[]
        print("before the loop")
        #yeta if pageno==1 garera tyo browser le deko page number check garera tyo session lai initialize garaune 
        #note tyo profile ma gayera back garda ali ghau vai raxa.
        latest_posts = Post.objects.filter(user=currentuser_profile_obj).order_by('-uploaded_date')


        for latest_post in latest_posts:
            if len(three_posts)<3:
                if int(latest_post.id)==int(request.session.get("f")) or int(latest_post.id)==int(request.session.get("s")) or int(latest_post.id)==int(request.session.get("t")):
                    print("paile ko ho yo")            
                elif int(latest_post.id)<int(request.session.get("t")):
                    three_posts.append(latest_post)
                elif int(latest_post.id)>int(request.session["f"]):
                    print("mathi nahi badega only tala")
            else:
                break

        print("after the loop")
        print(three_posts)

        follow_status=[]#yesma 3 ta element hunxa josle k vanxa vani yo current user chai tyo post ko author lai follow garya xa ki xaina
        for posts in three_posts:
            print("follow vitra")
            post_author_obj=posts.user
            is_following = Follow.objects.filter(follower=currentuser_profile_obj, following=post_author_obj).exists()
            if is_following:
                follow_status.append("unfollow")
            else:
                follow_status.append("follow")

        print("follow bahira")
        

        like_status=[]
        for posts in three_posts:
            has_like=Like.objects.filter(post=posts,user=currentuser_profile_obj).exists()
            if has_like:
                like_status.append("has_liked")
            else:
                like_status.append("has_not")
        
        comment_count=[]
        like_count=[]
        for posts in three_posts:
            c_count=Comment.objects.filter(post=posts).count()
            l_count=Like.objects.filter(post=posts).count()
            like_count.append(l_count)
            comment_count.append(c_count)
            


        if len(three_posts)==0:#or yesma tyo session lai reassign garera feri first batai data lina pani sakinxa
            print("the session is not changed. as it is was previous")
        if len(three_posts)==1:
            request.session["f"] = three_posts[0].id
            request.session["s"] = three_posts[0].id
            request.session["t"] =three_posts[0].id
        if len(three_posts)==2:
            request.session["f"] = three_posts[0].id
            request.session["s"] = three_posts[0].id
            request.session["t"] =three_posts[1].id 
        if len(three_posts)==3:
            request.session["f"] = three_posts[0].id
            request.session["s"] = three_posts[1].id
            request.session["t"] =three_posts[2].id                 


        print("assign garesi")
        print(request.session["f"])
        print(request.session["s"])
        print(request.session["t"])

        serializer=PostSerializer(three_posts,many=True)
        print('ok')
        return Response({'posts':serializer.data,'follow_status':follow_status,'like_status':like_status,"comment_count":comment_count,"like_count":like_count},status=200)
    except:
        return Response('sorry',status=500)




#######for the following feed------------
@login_required(login_url="/")
def following_feed(request):
    if request.method=="GET":
##########################################################################
        request.session["first"] = "3000"#note this is temporary. yeslai api call mai if halera assign garne
        request.session["second"] ="2000"
        request.session["third"] ="1500"
###########################################################################
        return render(request,'firstapp/following_feed.html')
    else:
        return HttpResponse("only get method allowed!!!")




 ###for the retrieval of the posts of the following person only(for following post section)
@api_view(['GET'])
def load_following_posts(request):
    try:   
        currentuser_profile_obj=UserProfile.objects.get(username=request.user.username)# Assuming the user is logged in, get the UserProfile
        
        three_posts=[]
        print("before the loop")
        #yeta if pageno==1 garera tyo browser le deko page number check garera tyo session lai initialize garaune 
        #note tyo profile ma gayera back garda ali ghau vai raxa.

        # Get the users the current user is following
        following_users = Follow.objects.filter(follower=currentuser_profile_obj).values_list('following', flat=True)

            # Get the posts from the users being followed and sort by date
        latest_posts= Post.objects.filter(user__id__in=following_users).order_by('-uploaded_date')

        for latest_post in latest_posts:
            if len(three_posts)<3:
                if int(latest_post.id)==int(request.session.get("first")) or int(latest_post.id)==int(request.session.get("second")) or int(latest_post.id)==int(request.session.get("third")):
                    print("paile ko ho yo")            
                elif int(latest_post.id)<int(request.session.get("third")):
                    three_posts.append(latest_post)
                elif int(latest_post.id)>int(request.session["first"]):
                    print("mathi nahi badega only tala")
            else:
                break

        print("after the loop")
        print(three_posts)

        follow_status=[]#yesma 3 ta element hunxa josle k vanxa vani yo current user chai tyo post ko author lai follow garya xa ki xaina
        for posts in three_posts:
            print("follow vitra")
            post_author_obj=posts.user
            is_following = Follow.objects.filter(follower=currentuser_profile_obj, following=post_author_obj).exists()
            if is_following:
                follow_status.append("unfollow")
            else:
                follow_status.append("follow")

        print("follow bahira")
        

        like_status=[]
        for posts in three_posts:
            has_like=Like.objects.filter(post=posts,user=currentuser_profile_obj).exists()
            if has_like:
                like_status.append("has_liked")
            else:
                like_status.append("has_not")
        
        comment_count=[]
        like_count=[]
        for posts in three_posts:
            c_count=Comment.objects.filter(post=posts).count()
            l_count=Like.objects.filter(post=posts).count()
            like_count.append(l_count)
            comment_count.append(c_count)
            


        if len(three_posts)==0:#or yesma tyo session lai reassign garera feri first batai data lina pani sakinxa
            print("the session is not changed. as it is was previous")
        if len(three_posts)==1:
            request.session["first"] = three_posts[0].id
            request.session["second"] = three_posts[0].id
            request.session["third"] =three_posts[0].id
        if len(three_posts)==2:
            request.session["first"] = three_posts[0].id
            request.session["second"] = three_posts[0].id
            request.session["third"] =three_posts[1].id 
        if len(three_posts)==3:
            request.session["first"] = three_posts[0].id
            request.session["second"] = three_posts[1].id
            request.session["third"] =three_posts[2].id                 


        print("assign garesi")
        print(request.session["first"])
        print(request.session["second"])
        print(request.session["third"])

        serializer=PostSerializer(three_posts,many=True)
        print('ok')
        return Response({'posts':serializer.data,'follow_status':follow_status,'like_status':like_status,"comment_count":comment_count,"like_count":like_count},status=200)
    except:
        return Response('sorry',status=500)        



###-------------for the fans section-----
@login_required(login_url="/")
def fans(request):
    if request.method=="GET":
        current_user_profile = UserProfile.objects.get(user=request.user)

        # Get all the followers of the current user
        followers = Follow.objects.filter(following=current_user_profile)

        # Extract the user profiles from the followers
        follower_profiles = [follower.follower for follower in followers]#follower_profiles is a list of user pofiles
        return render(request,"firstapp/fans.html",{"peoples":follower_profiles})
    else:
        return HttpResponse("sorry only get method is allowed")


    
    
    




####for the crop detail##########################
@login_required(login_url="/")
def crop_detail(request,name):
    if request.method=="GET":
       crop_object=CropInfo.objects.get(name=name)
       return render(request,"firstapp/cropDetail.html",{"crop":crop_object})





#####for the crop diesease prediction#########
@login_required(login_url="/")   
def predict_crop_portal(request):
    return render(request,"firstapp/dieseasepred_form.html")




# Load and preprocess the image for prediction
@login_required(login_url="/")
def preprocess_image(image):
    new_size = (256, 256)
    resized_image_pil = image.resize(new_size, Image.LANCZOS)
    resized_image_array_pil = np.array(resized_image_pil)
    resized_image_array_pil = resized_image_array_pil / 255.0  # Normalize pixel values to be between 0 and 1
    resized_image_array_pil = np.expand_dims(resized_image_array_pil, axis=0)  # Add batch dimension
    return resized_image_array_pil


import base64
from io import BytesIO
@api_view(["POST"])
def predict_crop_disease(request):
    if request.method == 'POST':
        crop = request.data['selectedCrop']
        print(crop)
        data = request.data['imageData']
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(BytesIO(image_data))
        new_size = (256, 256)
        resized_image_pil = image.resize(new_size, Image.LANCZOS)
        resized_image_array_pil = np.array(resized_image_pil)
        resized_image_array_pil = resized_image_array_pil / 255.0  # Normalize pixel values to be between 0 and 1
        resized_image_array_pil = np.expand_dims(resized_image_array_pil, axis=0)  # Add batch dimension
        if crop=="strawberry":
            predictions = modelstraw.predict(resized_image_array_pil)
            predicted_class_index = np.argmax(predictions, axis=1)
            class_names=['Strawberry___Leaf_scorch', 'Strawberry___healthy']
            predicted_class_name = class_names[predicted_class_index[0]]
            print("Predicted Class:", predicted_class_name)
        elif crop=="corn":
            predictions = modelcorn.predict(resized_image_array_pil)
            predicted_class_index = np.argmax(predictions, axis=1)
            class_names=['Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy']
            predicted_class_name = class_names[predicted_class_index[0]]
            print("Predicted Class:", predicted_class_name)
        elif crop=="grape":
            predictions = modelgrape.predict(resized_image_array_pil)
            print(predictions)
            predicted_class_index = np.argmax(predictions, axis=1)
            class_names=  ['Grape___Black_rot', 'Grape___Esca_(Black_Measles)','Grape___Leaf_blight_(Isariopsis_Leaf_Spot)','Grape___healthy']
            predicted_class_name = class_names[predicted_class_index[0]]
            print("Predicted Class:", predicted_class_name)
        elif crop=="apple":
            predictions = modelapple.predict(resized_image_array_pil)
            print(predictions)
            predicted_class_index = np.argmax(predictions, axis=1)
            class_names= ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy']
            predicted_class_name = class_names[predicted_class_index[0]]
            print("Predicted Class:", predicted_class_name)
        elif crop=="potato":
            predictions = modelapple.predict(resized_image_array_pil)
            print(predictions)
            predicted_class_index = np.argmax(predictions, axis=1)
            class_names= ['Early_Blight', 'Healthy', 'Late_Blight']
            predicted_class_name = class_names[predicted_class_index[0]]
            print("Predicted Class:", predicted_class_name)
        return Response(predicted_class_name)
    else:
        return Response({'success': False, 'message': 'Form is not valid'})
    




# -----for the home page making django as proxy

import requests
from django.http import JsonResponse
def news_api_proxy(request):
    API_KEY = "795eb89bf65c48929b9b1aa1256423e9"
    query = request.GET.get('q', 'Agriculture')
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}'

    response = requests.get(url)
    data = response.json()

    return JsonResponse(data)


##---------crop recommendation----------------
import numpy as np
import pandas
import joblib
from sklearn.preprocessing import StandardScaler, MinMaxScaler
# Load the trained model and scalers
model = joblib.load('F:/vs code/farmer/testhtmls/model.joblib')
scaler_standard = joblib.load('F:/vs code/farmer/testhtmls/scaler_standard.joblib')
scaler_minmax = joblib.load('F:/vs code/farmer/testhtmls/scaler_minmax.joblib')


##for the crop recommendation part
@login_required(login_url="/")
def recommend(request):
    if(request.method=="POST"):
        N = float(request.POST['Nitrogen'])
        P = float(request.POST['Phosporus'])
        K = float(request.POST['Potassium'])
        temperature = float(request.POST['Temperature'])
        humidity = float(request.POST['Humidity'])
        ph = float(request.POST['Ph'])
        rainfall = float(request.POST['Rainfall'])
        if N>150 or N<0 or ph>11 or ph<0 or P<5 or P>150 or K>210 or K<5 or temperature<0 or temperature>45 or humidity<10 or humidity>100 or rainfall>340 or rainfall<15:
            return render(request, 'firstapp/cropRecommendation.html', {"result":"no suitable crop"})
        
        # Transform input features
        features = [[N, P, K, temperature, humidity, ph, rainfall]]
        features_standardized = scaler_standard.transform(features)
        features_minmax = scaler_minmax.transform(features_standardized)
        # Make predictions
        predicted_crop = model.predict(features_minmax)[0]
        print(predicted_crop)
        class_probabilities = model.predict_proba(features_minmax)[0]
        print(class_probabilities)
        #probability_of_predicted_class = class_probabilities.max()


        # crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
        #             8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
        #             14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
        #             19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        result =predicted_crop
        return render(request, 'firstapp/cropRecommendation.html', {"result": result})
    else:
        return render(request, 'firstapp/cropRecommendation.html')




















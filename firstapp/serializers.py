from rest_framework import serializers
from .models import Post,UserProfile,Comment



# class PeopleSerializer(serializers.ModelSerializer):
#     #Meta class is used to specify the associated model (Person) and the fields that should be included in the serialization.
    
#     class Meta:
#         model=Person
#         # fields=['name','age','a',]#yesto garna saknxa particular field lai matra serialize hanna xa vani
#         fields='__all__'#sab field lai serialize garne vaneko ho

#     def validate(self,data):#This is a custom validation method that is called during the validation phase when you invoke serializer.is_valid()
#         #It checks if the value of the 'age' field in the data is less than 18. If it is, a serializers.ValidationError is raised with the provided message.
#         #If the validation succeeds, the validated data is returned.
#         if data['age']<18:
#             raise serializers.ValidationError('age should be greater than 18')#yo vaneko nearest exception handler ma yesle control pass gareko ho
#         return data


#     name=serializers.CharField(max_length=100)
#     age=serializers.IntegerField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'


class PostSerializer(serializers.ModelSerializer):
    user=UserProfileSerializer()
    class Meta:
        model=Post
        fields='__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    user=UserProfileSerializer()
    class Meta:
        model=Comment
        fields='__all__'
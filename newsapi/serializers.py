from mainapp.models import *
from rest_framework import serializers
from django.contrib.auth.models import User

#Login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False)
    password = serializers.CharField(allow_null=False)


#User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','phone','dob','gender','address']


#User data post
class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','phone','dob','gender','address']


#User serializer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone','dob','gender','address']


        #For News
class NewsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = News 
        fields = ["title", "subtitle", "slug", "category", "image", "text", "author"]


        #For NewsCategory
class NewsCategorySerializer(serializers.ModelSerializer):  

    class Meta:
        model = NewsCategory
        fields = ["title", "slug", "text", "image"]



class NewsCommentSerializer(serializers.ModelSerializer):  
    class Meta:
        model = NewsComment
        fields = ["name", "text", "image", "email", "news"]


class AdsCategorySerializer(serializers.ModelSerializer):  
    class Meta:
        model = AdsCategory
        fields = ["title", "slug"]


class AdsSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Ads
        fields = ["title", "issue_date", "end_date", "image", "sponsorship", "ads_category"]


class StaffSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Staff
        fields = ["name", "post", "profile", "education", "phone", "DoB"]


class ContactSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]

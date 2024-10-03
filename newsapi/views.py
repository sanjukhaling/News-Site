from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
import base64
import os
import random
from datetime import datetime
from io import BytesIO
from PIL import Image
# For Login 
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = authenticate(username=email, password=password)
            
            if user is not None:
                if user.is_active:
                    # Create and return the access token
                    access_token = AccessToken.for_user(user)
                    resp = {
                        "access": str(access_token),
                        "message": "Login successful."
                    }
                    return Response(resp, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Pending or suspended account."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Missing information."}, status=status.HTTP_400_BAD_REQUEST)


class GetAccessAPIView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            if user.is_active:
                tkn = AccessToken.for_user(user)
                resp = {
                    "my_token": str(tkn)
                }
                return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User account is inactive."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#User list
class UserListAPIView(APIView):

    def get(self,request):
        # users = User.objects.all()

        users = User.objects.raw("SELECT * FROM amsapp_user")

        # for pagination
        page = self.pagination_class.paginate_queryset(queryset=users, request=request)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            resp = {
                "status": "success",
                "data": serializer.data
            }
            if not users:
                resp = {
                "status": "User not found",
                }
            return self.pagination_class.get_paginated_response(resp)
        

# User Post View
class UserPostAPIView(APIView):

    def post(self, request):
        serializer = UserPostSerializer(data=request.POST)
        if not serializer.is_valid():
            # serializer.save()
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
            # return render(request, self.template_name,{'form':form,'smg_error':'Invalid form'})

        try:
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            phone = serializer.validated_data.get('phone')
            dob = serializer.validated_data.get('dob')
            gender = serializer.validated_data.get('gender')
            address = serializer.validated_data.get('address')
            user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,phone=phone,dob=dob,gender=gender,address=address)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e,"Errorrrrrrrrrr")
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

            # return render(request,self.template_name,{'forms':form,'msg_error':"Invalid Input"})

#User Update 
class UserUpdateAPIView(APIView):

    def get(self,request, id):
        try:
            user = User.objects.get(id=id)
            serializer=UserUpdateSerializer(user)
            return Response(serializer.data)
        
        except Exception as e:
            print(e,"Errorrrrr####")

    def put(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserUpdateSerializer(user,data=request.POST)
        if serializer.is_valid():
            serializer = serializer.save()
            serialized = UserUpdateSerializer(serializer)
            return Response(serialized.data,status=status.HTTP_201_CREATED)


#user delete
class UserDeleteAPIView(APIView):

    def get(self,request, id):
        try:
            user = User.objects.get(id=id)
            serializer=UserSerializer(user)
            return Response(serializer.data)
        
        except Exception as e:
            print(e,"Errorrrrr####")

    
    def delete(self,request,id):
        user = User.objects.get(id=id)
        user.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)
 




    #  List API 
class NewsListAPIView(APIView):

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


    # News Detail API
class NewsDetailAPIView(APIView):
    def get(self, request, id):
        try:
            news = News.objects.get(id=id)
            return Response({'status': 'success', 'data': NewsSerializer(news).data}, status=status.HTTP_200_OK)
        except News.DoesNotExist:
            return Response({'status': 'error', 'message': 'News not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Handle your POST request data as needed
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    #for create
class NewsCreateAPIView(APIView):

    def base64_to_image(self, base64_string, file_path):
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Decode the base64 string into bytes
            image_bytes = base64.b64decode(base64_string)

            # Create a BytesIO object to work with the binary data
            image_buffer = BytesIO(image_bytes)

            # Open the image using the Python Imaging Library (PIL)
            image = Image.open(image_buffer)

            random_integer = random.randint(100, 999)
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
            image_name = f"st-{formatted_date}-{random_integer}.jpg"

            # Save the image to a file
            image_saved_file = image.save(f"{file_path}/{image_name}", "JPEG")

            return f"{file_path}/{image_name} ,{image_saved_file}"
        except Exception as e:
            print(f"Error: {e}")


    def post(self, request):
        try:

            file_path = "/app/media/News/"
            photo = self.base64_to_image(request.data.get('image'), file_path)
            image_data = request.data.copy()  # Creates a mutable copy of the QueryDict
            image_data['image'] = photo

            serializer = NewsSerializer(data=image_data)

            if serializer.is_valid():
                serializer.save()
                res = {
                    'status': 'success',
                    'data': serializer.data
                }
            else:
                res = {
                    'message': serializer.errors
                }

            return Response(res)
        except Exception as e:
            print("Exception:",e)
            return



    #for Update API
class NewsUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            news = News.objects.get(id=id)
            serializer = NewsSerializer(news, data=request.data)  # Use correct serializer name
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except News.DoesNotExist:
            return Response({
                'status': 'News not found.',
            }, status=status.HTTP_404_NOT_FOUND)



    #for Delete API
class NewsDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            news = News.objects.get(id=id)
            news.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except News.DoesNotExist:
            return Response({
                'status': 'Deleting errors',
            }, status=status.HTTP_400_BAD_REQUEST)



        #NEWS-CATEGORY
    # List API
class NewsCategoryListAPIView(APIView):

    def get(self, request):
        news = NewsCategory.objects.all()
        serializer = NewsCategorySerializer(news, many=True)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


  #for Update API
class NewsCategoryUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            newscat = NewsCategory.objects.get(id=id)
            serializer = NewsCategorySerializer(newscat, data=request.data)  # Use correct serializer name
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NewsCategory.DoesNotExist:
            return Response({
                'status': 'NewsCategory not found.',
            }, status=status.HTTP_404_NOT_FOUND)


        #for NewsCategory
class NewsCategoryCreateAPIView(APIView):
    def post(self, request):
        try:

            file_path = "/app/media/newscategory"
            photo = self.base64_to_image(request.data.get('image'), file_path)

            # Extract only the relative path for the database
            relative_image_path = f"newscategory/{os.path.basename(photo)}"  # Get just the filename

            image_data = request.data.copy()
            image_data['image'] = relative_image_path  # Save only the relative path
            
            serializer = NewsCategorySerializer(data=image_data)

            if serializer.is_valid():
                serializer.save()
                res = {
                    'status': 'success',
                    'data': serializer.data
                }
            else:
                res = {
                    'message': serializer.errors
                }

            return Response(res)
        except Exception as e:
            print("Exception:",e)
            return



    def base64_to_image(self, base64_string, file_path):
        try:

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Decode the base64 string into bytes
            image_bytes = base64.b64decode(base64_string)

            # Create a BytesIO object to work with the binary data
            image_buffer = BytesIO(image_bytes)

            # Open the image using the Python Imaging Library (PIL)
            image = Image.open(image_buffer)
            random_integer = random.randint(100, 999)
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
            image_name = f"newscat-{formatted_date}-{random_integer}.jpg"

            # Save the image to a file

            # image_saved_file = image.save(f"{file_path}/{image_name}", "JPEG")
            # return f"{file_path}/{image_name}"

            # Save the image to a file
            image.save(os.path.join(file_path, image_name), "JPEG")

            # Return the full path of the saved image
            return os.path.join(file_path, image_name)
        
        except Exception as e:
            print(f"Error: {e}")


            
# NewsCategory Delete API
class NewsCatDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            newscat = NewsCategory.objects.get(id=id)
            newscat.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except NewsCategory.DoesNotExist:
            return Response({
                'status': 'Deleting errors',
            }, status=status.HTTP_400_BAD_REQUEST)



# NewsCat Detail API
class NewsCatDetailAPIView(APIView):
    def get(self, request, id):
        try:
            news = NewsCategory.objects.get(id=id)
            return Response({'status': 'success', 'data': NewsCategorySerializer(news).data}, status=status.HTTP_200_OK)
        except NewsCategory.DoesNotExist:
            return Response({'status': 'error', 'message': 'NewsCategory not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # No base64 image handling, expect normal image upload via request.FILES
        serializer = NewsCategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



#### NewsComments###
    #for create
class NewsCommentCreateAPIView(APIView):
    def post(self, request):
        try:

            file_path = "/app/media/commentprofile/"
            photo = self.base64_to_image(request.data.get('image'), file_path)
            image_data = request.data.copy()  # Creates a mutable copy of the QueryDict
            image_data['image'] = photo
            serializer = NewsCommentSerializer(data=image_data)

            if serializer.is_valid():
                serializer.save()
                res = {
                    'status': 'success',
                    'data': serializer.data
                }
            else:
                res = {
                    'message': serializer.errors
                }

            return Response(res)
        except Exception as e:
            print("Exception:",e)
            return



    def base64_to_image(self, base64_string, file_path):
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Decode the base64 string into bytes
            image_bytes = base64.b64decode(base64_string)

            # Create a BytesIO object to work with the binary data
            image_buffer = BytesIO(image_bytes)

            # Open the image using the Python Imaging Library (PIL)
            image = Image.open(image_buffer)

            ########################only for file name##################
            random_integer = random.randint(100, 999)
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
            image_name = f"st-{formatted_date}-{random_integer}.jpg"

            # Save the image to a file
            image_saved_file = image.save(f"{file_path}/{image_name}", "JPEG")

            return f"{file_path}/{image_name}"
        except Exception as e:
            print(f"Error: {e}")


#NewsCategory List API
class NewscommentListAPIView(APIView):

    def get(self, request):
        news_comment = NewsComment.objects.all()
        serializer = NewsCommentSerializer(news_comment, many=True)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


        #for  Update API
class NewsCommentUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            newscomment = NewsComment.objects.get(id=id)
            serializer = NewsCommentSerializer(newscomment, data=request.data)  # Use correct serializer name
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NewsComment.DoesNotExist:
            return Response({
                'status': 'NewsComment not found.',
            }, status=status.HTTP_404_NOT_FOUND)



    # Delete API
class NewsCommentsDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            newscat = NewsComment.objects.get(id=id)
            newscat.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except NewsComment.DoesNotExist:
            return Response({
                'status': 'Deleting errors',
            }, status=status.HTTP_400_BAD_REQUEST)


#           #for  Detail API
class NewsCommentDetailAPIView(APIView):
    def get(self, request, id):
        try:
            news = NewsComment.objects.get(id=id)
            return Response({'status': 'success', 'data': NewsCommentSerializer(news).data}, status=status.HTTP_200_OK)
        except NewsComment.DoesNotExist:
            return Response({'status': 'error', 'message': 'NewsComment not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # No base64 image handling, expect normal image upload via request.FILES
        serializer = NewsCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    #Ads Category#
    #for create
class AdsCatCreateAPIView(APIView):
    def post(self, request):
        try:
            # Handle request data without any image processing
            serializer = AdsCategorySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'data': serializer.data})
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception:", e)
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Ads List API
class AdsCatListAPIView(APIView):

    def get(self, request):
        news_ads = AdsCategory.objects.all()
        serializer = AdsCategorySerializer(news_ads, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


# Ads Update API
class AdsCatUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            news_ads = AdsCategory.objects.get(id=id)
            serializer = AdsCategorySerializer(news_ads, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdsCategory.DoesNotExist:
            return Response({
                'status': 'ads not found.',
            }, status=status.HTTP_404_NOT_FOUND)


# Ads Delete API
class AdsCatDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            news_ads = AdsCategory.objects.get(id=id)
            news_ads.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except AdsCategory.DoesNotExist:
            return Response({
                'status': 'Deleting errors',
            }, status=status.HTTP_400_BAD_REQUEST)


# Ads Detail API
class AdsCatDetailAPIView(APIView):
    def get(self, request, id):
        try:
            ads_cat = AdsCategory.objects.get(id=id)
            return Response({'status': 'success', 'data': AdsCategorySerializer(ads_cat).data}, status=status.HTTP_200_OK)
        except AdsCategory.DoesNotExist:
            return Response({'status': 'error', 'message': 'ads not found.'}, status=status.HTTP_404_NOT_FOUND)


    #Ads 
class AdsCreateAPIView(APIView):

    def base64_to_image(self, base64_string, file_path):
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Decode the base64 string into bytes
            image_bytes = base64.b64decode(base64_string)

            # Create a BytesIO object to work with the binary data
            image_buffer = BytesIO(image_bytes)

            # Open the image using the Python Imaging Library (PIL)
            image = Image.open(image_buffer)

            random_integer = random.randint(100, 999)
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
            image_name = f"st-{formatted_date}-{random_integer}.jpg"

            # Save the image to a file
            image_saved_file = image.save(f"{file_path}/{image_name}", "JPEG")

            return f"{file_path}/{image_name} ,{image_saved_file}"
        except Exception as e:
            print(f"Error: {e}")


    def post(self, request):
        try:

            file_path = "/app/media/ads/"
            photo = self.base64_to_image(request.data.get('image'), file_path)
            image_data = request.data.copy()  # Creates a mutable copy of the QueryDict
            image_data['image'] = photo

            serializer = AdsSerializer(data=image_data)

            if serializer.is_valid():
                serializer.save()
                res = {
                    'status': 'success',
                    'data': serializer.data
                }
            else:
                res = {
                    'message': serializer.errors
                }

            return Response(res)
        except Exception as e:
            print("Exception:",e)
            return


#Ads List API
class AdsListAPIView(APIView):

    def get(self, request):
        news_ads = Ads.objects.all()
        serializer = AdsSerializer(news_ads, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)



# Ads Update API
class AdsUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            news_ads = Ads.objects.get(id=id)
            serializer = AdsSerializer(news_ads, data=request.data)  # Use correct serializer name
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ads.DoesNotExist:
            return Response({
                'status': 'ads not found.',
            }, status=status.HTTP_404_NOT_FOUND)



# Ads Delete API
class AdsDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            news_ads = Ads.objects.get(id=id)
            news_ads.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Ads.DoesNotExist:
            return Response({
                'status': 'Deleting errors',
            }, status=status.HTTP_400_BAD_REQUEST)


# Ads Detail API
class AdsDetailAPIView(APIView):
    def get(self, request, id):
        try:
            ads = Ads.objects.get(id=id)
            return Response({'status': 'success', 'data': AdsSerializer(ads).data}, status=status.HTTP_200_OK)
        except Ads.DoesNotExist:
            return Response({'status': 'error', 'message': 'ads not found.'}, status=status.HTTP_404_NOT_FOUND)




    #STAFF#
#for staff
class StaffCreateAPIView(APIView):
    def base64_to_image(self, base64_string, file_path):
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Decode the base64 string into bytes
            image_bytes = base64.b64decode(base64_string)

            # Create a BytesIO object to work with the binary data
            image_buffer = BytesIO(image_bytes)

            # Open the image using the Python Imaging Library (PIL)
            image = Image.open(image_buffer)

            random_integer = random.randint(100, 999)
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
            image_name = f"st-{formatted_date}-{random_integer}.jpg"

            # Save the image to a file
            image_saved_file = image.save(f"{file_path}/{image_name}", "JPEG")

            return f"{file_path}/{image_name} ,{image_saved_file}"
        except Exception as e:
            print(f"Error: {e}")


    def post(self, request):
        try:

            file_path = "/app/media/staff/"
            photo = self.base64_to_image(request.data.get('image'), file_path)
            image_data = request.data.copy()  # Creates a mutable copy of the QueryDict
            image_data['image'] = photo

            serializer = StaffSerializer(data=image_data)

            if serializer.is_valid():
                serializer.save()
                res = {
                    'status': 'success',
                    'data': serializer.data
                }
            else:
                res = {
                    'message': serializer.errors
                }

            return Response(res)
        except Exception as e:
            print("Exception:",e)
            return


#Staff List API
class StaffListAPIView(APIView):

    def get(self, request):
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


# Staff Update API
class StaffUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            news_ads = Staff.objects.get(id=id)
            serializer = StaffSerializer(news_ads, data=request.data)  # Use correct serializer name
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Staff.DoesNotExist:
            return Response({
                'status': 'ads not found.',
            }, status=status.HTTP_404_NOT_FOUND)



# Staff Delete API
class StaffDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            news_ads = Staff.objects.get(id=id)
            news_ads.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Staff.DoesNotExist:
            return Response({
                'status': 'Deleting errors',
            }, status=status.HTTP_400_BAD_REQUEST)


# Staff Detail API
class StaffDetailAPIView(APIView):
    def get(self, request, id):
        try:
            staff = Staff.objects.get(id=id)
            return Response({'status': 'success', 'data': StaffSerializer(staff).data}, status=status.HTTP_200_OK)
        except Staff.DoesNotExist:
            return Response({'status': 'error', 'message': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Remove base64 handling, directly use the image from request data
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    #Contact
class ContactListAPIView(APIView):

    def get(self, request):
        news = Contact.objects.all()
        serializer = ContactSerializer(news, many=True)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


  #for Update API
class ContactUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            newscat = Contact.objects.get(id=id)
            serializer = ContactSerializer(newscat, data=request.data)  # Use correct serializer name
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contact.DoesNotExist:
            return Response({
                'status': 'NewsCategory not found.',
            }, status=status.HTTP_404_NOT_FOUND)


        #for NewsCategory
class ContactCreateAPIView(APIView):
    def post(self, request):
        try:
            # Use the request data directly without handling images
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'data': serializer.data})
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception:", e)
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# NewsCategory Delete API
class ContactDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            newscat = Contact.objects.get(id=id)
            newscat.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return Response({
                'status': 'Deleting errors',
            }, status=status.HTTP_400_BAD_REQUEST)



# NewsCat Detail API
class ContactDetailAPIView(APIView):
    def get(self, request, id):
        try:
            news = NewsCategory.objects.get(id=id)
            return Response({'status': 'success', 'data': ContactSerializer(news).data}, status=status.HTTP_200_OK)
        except NewsCategory.DoesNotExist:
            return Response({'status': 'error', 'message': 'NewsCategory not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # No base64 image handling, expect normal image upload via request.FILES
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

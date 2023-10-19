from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from accounts.serializers import UserLoginSerializer1,UserLoginSerializer2,ResetPasswordEmailRequestSerializer
from accounts.serializers import SetNewPasswordSerializer
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from rest_framework import generics
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.http import HttpResponsePermanentRedirect
import os



class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']
# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    if 'signin' in request.session:
      current_user = request.user
      user_data = current_user.id
      a= User.objects.filter(id=user_data)
      print('main object',a)
      for i in a:
        print(i.is_admin)
        x=a[0].is_admin
        print(a[0].is_admin,'-all data')
      
      serializer = UserRegistrationSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      if x=='1':
        print('admin creation')
        user1 = serializer.save()
        y=user1.is_admin = '2'
        print (y,'is_admin is 2')
        user = user1.save()
        print(user,"checkuser")
        # token = get_tokens_for_user(user)
        return Response({ 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
      print ('user creation')
      user = serializer.save()
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    else:      
      serializer = UserRegistrationSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      
        
      user = serializer.save()
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
      

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    x=request.data
    a=x['email'] 
    print(a)
    b=x['password']
    print(b)
    
    details = dict({"email":a,"password":b})
    details1 = dict({"username":a,"password":b})
    y= User.objects.filter(email=a)
    print(y,"hgikjh")
      
      
    if y.exists():
      
      user = User.objects.get(email = a)
      user1 = user.is_admin
      print(user1)
      serializer = UserLoginSerializer(data=details)
      serializer.is_valid(raise_exception=True)
      email = serializer.data.get('email')
      print(email,'email')
      password = serializer.data.get('password')
      print(password,'password')
      user = authenticate(username=email, password=password)
      print(user,'user')
      request.session['signin'] = email   
          
      if user is not None:
        token = get_tokens_for_user(user)
        token["privilege"]=str(user1)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

    else:
      print('checkgf')
      user = User.objects.get(username = a)
      user1 = user.is_admin
      print(user1)
      serializer = UserLoginSerializer1(data=details1)
      print(serializer,'check1')
      serializer.is_valid(raise_exception=True)
      username = a
      print(username,'username')
      password = serializer.data.get('password')
      print(password,'password')
      user = authenticate(username=username, password=password)
      print(user,'user')
      request.session['signin'] = username   
          
      if user is not None:
        token = get_tokens_for_user(user)
        token["privilege"]=str(user1)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Username or Password is not Valid  ']}}, status=status.HTTP_404_NOT_FOUND)

class UserLogin2View(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    x=request.data
    a=x['mobile'] 
    print(a)
  
    y= User.objects.filter(mobile=a)
    print(y,"hgikjh")
      
      
    if y.exists():
      print('check')
      user = User.objects.get(mobile = a)
      user1 = user.is_admin
      print(user1)
      serializer = UserLoginSerializer2(data=request.data)
      print(serializer,'check1')
      serializer.is_valid(raise_exception=True)
      username = serializer.data.get('mobile')
      print(username,'username')
      password = serializer.data.get('password')
      print(password,'password')
      user = authenticate(username=username, password=password)
      print(user,'user')
      request.session['signin'] = username   
          
      if user is not None:
        token = get_tokens_for_user(user)
        token["privilege"]=str(user1)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Mobile or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

    


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    current_user = request.user
    user_data = current_user.id
    print(user_data)
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def put(self, request, format=None):
        current_user = request.user
        user_data = current_user.id
       
        m=User.objects.get(id=user_data)
        
        serializer = UserProfileSerializer(m, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data) 
            # return Response({ 'msg':'update Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
      
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


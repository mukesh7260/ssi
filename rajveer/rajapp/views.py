
from django.shortcuts import render
from rajapp.serializers import EmployeeSerializer , ProductSerializer,RegisterSerializer,LogoutSerializer,LogSerializers,VerifyEmailOtpSerializer,ChangePasswordSerializer
from .utils import  *
from rest_framework.validators import ValidationError
from.models import Employee ,Product, PhoneOTP,UserOtp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from http import HTTPStatus
from.serializers import EmployeeSerializer, PhoneSerializer, ProductSerializer
from django.contrib.auth import authenticate
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views  import APIView
from django.shortcuts import  get_object_or_404
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

import random

from rest_framework import filters
from rest_framework.filters import SearchFilter
from re import sub
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from rajapp.forms import ProductForm 
from django.conf import settings
from rest_framework.permissions import AllowAny

from rajapp import serializers
User = get_user_model()


class RegisterViewset(viewsets.ViewSet):
    
    serializer_class=RegisterSerializer
    def create(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
        return Response(serializer.data)

    def list(self,request):
        queryset = User.objects.all()
        serializers = RegisterSerializer(queryset,many=True)
        return Response({'status':200,'payload':serializers.data}) 

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message":"Logout User Successfully"
        })

class LogiViewset(viewsets.ViewSet):
    serializer_class= LogSerializers
    def create(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get("phone")
        user = authenticate(username=username,password=password)
        user=User.objects.filter(username=username).first()
        usr_otp = random.randint(100000, 999999)
        if user is not None:
                if UserOtp.objects.filter(key_id=user.id).exists():
                        print(UserOtp.objects.update(otp = usr_otp)) 
                else:
                        mkr = UserOtp.objects.create(key_id=user.id, otp = usr_otp)
                        mkr.save()

                        
        elif phone is not None:
                try:
                        phone_number =  phone
                        print("jajasasdja",phone_number)
                        send_otp_to_phone(phone_number)
                        #return Response(send_otp_to_phone(phone_number))
                except Exception as e:
                     raise ValidationError({"phone": "Invalid phone number"})
                
         
        else:
                print("hello")
                mkr = UserOtp.objects.create(key_id=user.id, otp = usr_otp)
                mkr.save()
       
        mess = f"Hello {user.first_name},\nYour OTP is {usr_otp}\nThanks!"

        send_mail(
        "Welcome to Mukesh Developing Site through - Verify Your Email",
        mess,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently = False
        )
        # data= UserOtp.objects.update(otp = usr_otp)
        if    user is not None:
                user.is_active=False
                user.save()
                # return redirect("verify_otp")             
        if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "user":RegisterSerializer(user).data,
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        })
       
        
        return Response("Something went wrong!")

class VerifyOtpViewSet(APIView):
        def post(self, request):
                serializer =VerifyEmailOtpSerializer(data=request.data)
                if serializer.is_valid():
                        return Response({"detail":"OTP verified successfully"}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class EmployeeView(viewsets.ModelViewSet):
        filter_backends = (SearchFilter,)
        search_fields = ('^name', )
        queryset = Employee.objects.all()
        serializer_class = EmployeeSerializer

class ProductView(viewsets.ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
class PhoneView(viewsets.ModelViewSet):
        queryset = PhoneOTP.objects.all()
        serializer_class  =  PhoneSerializer




class LogoutApiview(APIView):	
	def post(self, request, format = None):
		try:
			refresh_token = request.data.get('refresh_token')
			token_obj = RefreshToken(refresh_token)
			token_obj.blacklist()
			return Response({"message": " Logout successfully"})
		except Exception as e:
			return Response({"message": "token has expired ! plesase take another token !!"})

             
          
               


# class ChangePasswordView(APIView):
#         permission_classes = [IsAuthenticated]
#         def post(self, request, format=None):
#                 serializer =ChangePasswordSerializer(data=request.data)
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
#                 return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
       

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

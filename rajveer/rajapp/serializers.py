from rest_framework import serializers
from.models import Employee, PhoneOTP, Product, UserOtp
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)
        class Meta:
                model = User

                fields = [ 
                        "username",
                        "email",
                        "first_name",
                        "last_name",
                        "password"
                ]
                # exctra_kwargs  ={"write_only" : True} 
        def create(self,validated_data):
                password=validated_data.pop('password',None)
                instance = self.Meta.model(**validated_data)
                if password is not None:
                        instance.set_password(password)
                instance.save()
                return instance  

class LogSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()  


class VerifyEmailOtpSerializer(serializers.Serializer):
        email = serializers.EmailField()
        otp = serializers.CharField(write_only=True)
        # class Meta:
        #         model=User
        #         fields = [ 
        #                 "email",
        #                 "otp"
        #         ]
        def validate_email(self, attrs):
                print("email")
                email = attrs
                try:
                        user=User.objects.filter(email=email).last()
                        email = user.email
                except:
                        raise ValidationError("related objects not found")
                if email != email:
                        raise ValidationError({"errors": "Invalid email"})
                user.is_active=True
                user.save()
                return attrs
        def validate_otp(self,attrs):
                print("phone")
                otp = attrs
                print(otp,"*****************")

                try:
                        otp_obj = UserOtp.objects.filter(otp=otp).last()
                        print(otp_obj,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                        obj_otp = otp_obj.otp
                        
                       
                except:
                        raise ValidationError("related objects not found !!!!")
                       
                if obj_otp != otp :
                        raise ValidationError("Invalid otp")
                
                
                return attrs


class EmployeeSerializer(serializers.ModelSerializer):
        class Meta:
                model = Employee
                fields = [ 'id', 'name' , 'designation']
                # depth = 1

class ProductSerializer(serializers.ModelSerializer):
        # emp =EmployeeSerializer(write_only= True,many=True)
        class Meta:
                model = Product
                fields = ['id' ,'product_name' , 'desc' , 'emp']

class PhoneSerializer(serializers.ModelSerializer):
        class Meta:
                model = PhoneOTP
                fields = ['email','otp','password']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": "Token is expired or invalid"}

    def validate(self, attrs):
        self.token = attrs['refresh_token'] 
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")


class ChangePasswordSerializer(serializers.Serializer):
        opassword = serializers.CharField(required = True)
        npassword = serializers.CharField(required = True) 

        # model = User
        # class Meta:
        #         model = User
        #         fields = ['opassword','npassword']

        # def validate(self, attrs):
        #         opassword = attrs.get('opassword') 
        #         npassword = attrs.get('npassword')
        #         if opassword != npassword:
        #                 raise serializers.ValidationError('opassword and npassword does not matche, so entre correct password') 
                
        #         return attrs 
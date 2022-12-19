from django.contrib import admin
from .models import Employee ,Product, PhoneOTP,UserOtp


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
        list_display  =  ['id' , 'name' ,'designation']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
        list_display = ['id', 'product_name' ,'desc']

@admin.register( PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
        list_display =['email' ,'otp' ,'password']


class UserOtpAdmin(admin.ModelAdmin):
        list_display = ['otp','key']

admin.site.register(UserOtp,UserOtpAdmin)


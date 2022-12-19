from django import forms
from django.conf import settings
from django.core.mail import send_mail

class ProductForm(forms.Form):
        product_name =forms.CharField(required=True)
        desc  = forms.CharField(required=True)
       

        
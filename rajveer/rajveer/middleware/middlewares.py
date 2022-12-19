from rest_framework.response import Response
from requests.models import Response
from django.http import JsonResponse
import json
#from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class Checkmiddleware:
    def __inti__(self, get_response):
        self.get_response = get_response
        print('initilise middleware') 

    def __call__(self,request):
        print('I am before view processing')



        response = self.get_response(request)
        print('I am after viewing processing')



        return response
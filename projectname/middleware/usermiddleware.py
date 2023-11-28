import logging
from typing import Any
from django.http import HttpResponsePermanentRedirect

class mymiddleware:
    def __init__(self,get_response) :
        self.get_response = get_response

    def __call__(self, request) :
        response = self.get_response(request)
        #print("called")
        url=request.path
    
        print("url path:"+url)
        print(not request.user.is_authenticated)
        print(not (url.endswith('login/') or url.endswith ('register/') or url == '/'))
        if not request.user.is_authenticated:
        #return
            print("in if")
            if not (url.endswith('login/') or url.endswith ('register/') or url == '/'):
              print("in inner if")
              return HttpResponsePermanentRedirect('http://localhost:8000/register/')
        return response
    
    def process_view(self,request,view_func,view_args,view_kwargs):
        #this code is executed just before view is called
        pass

    def process_exception(self,request,exception):
        #this code is executed if an exception is raised
        pass

    def process_template_response(self,request,response):
        #this code is executed if the response contains a render() method
        return response
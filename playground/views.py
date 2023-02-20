from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request -> response
# request handler
# action
# django calls this a "view"

def say_hello(request):
    # pull data from db
    # send email, etc
    #return HttpResponse('Mohana says Hello world')
    return render(request, 'hello.html',{'name':'Ye'})
    #return render(request, 'home.html')
    
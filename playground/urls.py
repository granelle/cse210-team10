from django.urls import path
from . import views

# URL config model
# URLConf
urlpatterns = [
    path('hello/', views.say_hello)
]
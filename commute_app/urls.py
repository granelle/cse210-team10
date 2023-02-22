from django.urls import path
from . import views

# URL config model
# URLConf
urlpatterns = [
    path('home/', views.go_home),
    path('scores/', views.search_near_home, name = "scores"),
    path('tutorial/', views.display_tutorial),
    path('error/', views.display_error)
]
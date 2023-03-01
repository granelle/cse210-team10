from django.urls import path
from . import views

# URL config model
# URLConf
urlpatterns = [
    path('home/', views.go_home, name = "home"),
    path('scores/', views.display_scores, name = "scores"),
    path('tutorial/', views.display_tutorial, name = 'tutorial'),
    path('error/', views.display_error)
]
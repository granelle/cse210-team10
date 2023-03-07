from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib import admin


# URL config model
# URLConf
urlpatterns = [
    path('home/', views.go_home, name = "home"),
    path('scores/', views.display_scores, name = "scores"),
    path('tutorial/', views.display_tutorial, name = 'tutorial'),
    path('error/', views.display_error),
    path('admin/', admin.site.urls),
    path("accounts/signup", views.display_signup.as_view(), name = 'signup'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
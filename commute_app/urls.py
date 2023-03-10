from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib import admin


# URL config model
# URLConf
urlpatterns = [
    path('home/', views.go_home, name = "home"),
    path('rating/', views.display_scores, name = "rating"),
    path('tutorial/', views.display_tutorial, name = 'tutorial'),
    path('contact/', views.display_contact, name = 'contact'),
    path('error/', views.display_error),
    #Mohana database testing
    path('database_test/', views.database_test),
    path('admin/', admin.site.urls),
    path("accounts/signup", views.display_signup.as_view(), name = 'signup'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('favorite/', views.display_favorite, name = "favorite"),
]
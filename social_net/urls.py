"""social_net URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

API_BASE = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_BASE + 'auth/', include('dj_rest_auth.urls')),
    path(API_BASE + 'auth/registration/', include('dj_rest_auth.registration.urls')),

    path(API_BASE + 'posts/', include('posts.urls'), name='posts'),
    path(API_BASE + 'likes/', include('likes.urls'), name='likes'),
    path(API_BASE + 'users/', include('users.urls'), name='users'),
]

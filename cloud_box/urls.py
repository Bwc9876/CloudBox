"""
URL configuration for cloud_box project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path, include
from main.views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('boxes/', BoxList.as_view(), name='box_list'),
    path("boxes/new/", BoxCreate.as_view(), name='box_create'),
    path("boxes/delete/<int:pk>/", BoxDelete.as_view(), name='box_delete'),
    path('register/', UserCreationView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]

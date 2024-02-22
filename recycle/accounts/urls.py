# accounts=urls.py
from django.urls import path
from accounts.views import LoginView
from django.urls import path, include #For Register
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
 

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  
    path('users/', UserViewSet.as_view,name='users'),
    

]

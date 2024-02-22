#from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings #Settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework .views import APIView  #Login
from rest_framework import viewsets   #Register
from .serializers import UserSerializer  #Register
from rest_framework.decorators import action  #Register
from rest_framework.response import Response
from accounts.email import send_otp_via_email
# from accounts.backend import AdminPhoneBackend #backend
from accounts.backend import PhoneBackend      #backend
from rest_framework import status
from django.utils import timezone
from accounts.models import UserModel
import random
import datetime

# For Login
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = UserModel.objects.get(email=email, is_active=1)

        except UserModel.DoesNotExist:
            return Response({'success':False,"message":"User does not exist.","status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        otp = random.randint(1000, 9999)
        
        otp_expiry = timezone.now() + datetime.timedelta(minutes=15)
        user.otp = otp
        user.otp_expiry = otp_expiry
        user.save()

        
        
        
    def send_otp_via_email(email, otp):
        return Response({'success':True,"data":{"id": user.id,"message":"OTP sent to user."},"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
#For Register
class UserViewSet(viewsets.ModelViewSet):
    """
    UserModel View.
    """

    queryset = UserModel.objects.filter(is_vendor=False)
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()
        if (instance.otp == request.data.get("otp")
            and (instance.otp_expiry is not None 
            and timezone.now() < instance.otp_expiry)
                ):
                instance.is_active = True
                instance.otp_expiry = None
                instance.max_otp_try = settings.MAX_OTP_TRY
                instance.otp_max_out = None
                instance.save()
                user, token = PhoneBackend().authenticate(request=request, phone_number=instance.phone_number)
                if user is not None:
                    login(request, user, backend='accounts.backend.PhoneBackend')
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse(
                    { 'success':True, 'token': token.key, 'message': "User logged in"},
                    status=status.HTTP_200_OK
                )
        elif not instance.is_active and instance.otp == request.data.get("otp") and timezone.now() < instance.otp_expiry:
                instance.is_active = True
                instance.otp_expiry = None
                instance.max_otp_try = settings.MAX_OTP_TRY
                instance.otp_max_out = None
                instance.save()
                user, token = PhoneBackend().authenticate(request=request, phone_number=instance.phone_number)
                if user is not None:
                    login(request, user, backend='accounts.backend.PhoneBackend')
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {'success':True,'token': token.key, 'message': "User logged in"},
                    status=status.HTTP_200_OK
                )
        return Response(
             
                {'success':False,"message":"Please enter the correct OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )
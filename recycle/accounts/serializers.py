from datetime import timedelta
import random 
import datetime
from django.conf import settings
from rest_framework import serializers
from accounts.email import send_otp_via_email
from .models import UserModel
from django.utils import timezone
from django.db import models

class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer.

    Used in POST and GET
    """
    class Meta:
        model = UserModel
        fields = (
            "id",
            "phone_number",
            "email",
            "name",
            "upiId",
            "pickup_otp"
        )
        read_only_fields = ("id","name","upiId")

    def to_internal_value(self, data):
        phone_number = data.get("phone_number")
        email = data.get("email")

        existing_user = UserModel.objects.filter(
            (models.Q(email=email) | models.Q(phone_number=phone_number)),
            is_active=False
        ).first()

        if existing_user:
            existing_user.delete()

        return super().to_internal_value(data)

 
    def create(self, validated_data):
        """
        Create method.

        Used to create the user
        """
        otp = random.randint(1000, 9999)
        otp_expiry = datetime.now() + timedelta(minutes = 10)
        otp_expiry = timezone.now() + timedelta(minutes=15)

        user = UserModel(
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            otp=otp,
            pickup_otp = random.randint(1000,9999),
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY,
        )
        user.save()
        send_otp_via_email(validated_data["email"], otp)
        return user
 
 
# class UserNameUpdateSerializer(serializers.ModelSerializer):
#     """
#     Serializer for updating the user's name.
#     """
#     class Meta:
#         model = UserModel
#         fields = ["name",'email','upiId']

# class VendorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ("id","phone_number", "email", "pincode", "is_vendor", "password", "name")
        
from django.db import models
from accounts.models import UserModel
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 10 digits only."
)
pincode_regex = RegexValidator(
    regex=r"^\d{6}", message="Pin code must be 6 digits only."
)

class Address(models.Model):
    contact_person_name = models.CharField(max_length=255)
    contact_person_number = models.CharField(max_length=10, null=False, blank=False, validators=[phone_regex])
    flat_number = models.CharField(max_length=50)
    area = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6, null=False, blank=False, validators=[pincode_regex])
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='addresses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address_type = models.CharField(max_length=10, choices=[('office', 'Office'), ('home', 'Home')])
    is_active = models.BooleanField(default=True)
    preferred = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # If preferred==True, sets preferred values of same user to False
        if self.preferred:
            Address.objects.filter(user=self.user, preferred=True).exclude(id=self.id).update(preferred=False)
        super(Address, self).save(*args, **kwargs)
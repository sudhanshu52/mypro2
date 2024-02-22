from django.urls import path
from .views import AddressListCreateView, AddressDetailView, SetPreferredAddressAPIView

urlpatterns = [
    # path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    path('users/<int:user_id>/addresses/', AddressListCreateView.as_view(), name='user-address-list-create'),
    path('set_preferred_address/<int:id>/', SetPreferredAddressAPIView.as_view(), name='set_preferred_address'),

]

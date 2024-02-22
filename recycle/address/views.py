from rest_framework import generics, status
from .models import Address
from .serializers import AddressSerializer
from rest_framework.response import Response

class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        if user_id is not None:
            return Address.objects.filter(user_id=user_id).order_by('-updated_at')
        return Address.objects.all().order_by('-updated_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'status': '200',
            'success': True,
            'message': 'Address List',
            'data': serializer.data
        }
        return Response(response_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'status': '201',
            'success': True,
            'message': 'Address added successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'status': '200',
            'success': True,
            'message': 'Address shown successfully',
            'data': serializer.data
        }
        return Response(response_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {
            'status': '200',
            'success': True,
            'message': 'Address updated successfully',
            'data': serializer.data
        }
        return Response(response_data)

class SetPreferredAddressAPIView(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    lookup_field = 'id'  

    def get_queryset(self):
        user_id = self.request.data.get('user')
        return Address.objects.filter(user__id=user_id)

    def update(self, request, *args, **kwargs):
        # Set the preferred flag to True for the provided address_id
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['preferred'] = True

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {
            'status': '200',
            'success': True,
            'message': 'Preffered address selected',
            'data': serializer.data
        }
        return Response(response_data)
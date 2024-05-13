from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Business
from .serializers import BusinessSerializer, BusinessListSerializer
from rest_framework.generics import ListAPIView


class BusinessRegistrationAPIView(APIView):
    """
        API endpoint for registering a business.

        POST:
        Register a new business using the provided data.

        Payload:
        {
            "name": "string, required",
            "email": "string, required",
            "address": "string, required",
            "phone": "string, required",
            "registration_number": "string required"
        }

        Returns:
        - If successful, returns API key and secret key.
        - If unsuccessful due to invalid data, returns detailed error messages.

        Status Codes:
        - 201 Created: Business registered successfully.
        - 400 Bad Request: Invalid data provided.
    """
    def post(self, request, format=None):
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            business_data = serializer.data
            return Response({'api_key': business_data['api_key'], 'secret_key': business_data['secret_key']},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessListAPIView(ListAPIView):
    """
        API endpoint for listing businesses.

        GET:
        Retrieve a list of all businesses.

        Returns:
        - List of serialized business data.

        Status Codes:
        - 200 OK: Successful retrieval.
    """
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Business
from .serializers import BusinessSerializer, BusinessListSerializer
from rest_framework.generics import ListAPIView


class BusinessRegistrationAPIView(APIView):
    def post(self, request, format=None):
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            business_data = serializer.data
            return Response({'api_key': business_data['api_key'], 'secret_key': business_data['secret_key']},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessListAPIView(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

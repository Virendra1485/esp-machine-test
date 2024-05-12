import jwt
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from .serializers import TokenRequestSerializer
from .serializers import UserRegistrationSerializer, UserUpdateSerializer, UserDeletionSerializer
from .models import User


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer


class TokenGenerationAPIView(APIView):
    serializer_class = TokenRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            user = User.objects.filter(phone=phone).first()
            if user and user.check_password(password):
                access_token = AccessToken.for_user(user)
                data = {
                    'token': str(access_token),
                    'api_key': user.api_key,
                    'secret_key': user.secret_key,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        authorization_header = self.request.headers.get('Authorization')
        if not authorization_header or 'Bearer ' not in authorization_header:
            return None

        token = authorization_header.split(' ')[1]

        try:
            decoded_token = AccessToken(token).payload
            user_id = decoded_token.get('user_id')
            if user_id:
                return User.objects.filter(id=user_id).first()
        except jwt.DecodeError:
            print("decode error")
        except jwt.ExpiredSignatureError:
            print("signature expired error")
        except jwt.InvalidTokenError:
            print("invalid token error")
        return None

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'error': 'Invalid or missing token'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = UserDeletionSerializer(data={}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.delete()
        return Response({'message': 'User deleted successfully'})

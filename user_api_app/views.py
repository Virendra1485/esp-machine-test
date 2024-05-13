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
    """
       API endpoint for user registration.

       POST:
       Register a new user using the provided data.

       Payload:
       {
           "name": "string, required",
           "email": "string, required",
           "password": "string, required",
           "phone": "string, required",
           "address": "string, required",
       }

       Returns:
       - If successful, returns serialized user data.
       - If unsuccessful due to invalid data, returns detailed error messages.

       Status Codes:
       - 201 Created: User registered successfully.
       - 400 Bad Request: Invalid data provided.
    """
    serializer_class = UserRegistrationSerializer


class TokenGenerationAPIView(APIView):
    """
        API endpoint for generating access tokens.

        POST:
        Generate an access token using the provided phone number and password.

        Payload:
        {
            "phone": "string, required",
            "password": "string, required"
        }

        Returns:
        - If successful and credentials are valid, returns token, API key, and secret key.
        - If unsuccessful due to invalid credentials or data, returns error messages.

        Status Codes:
        - 200 OK: Token generated successfully.
        - 400 Bad Request: Invalid data provided.
        - 401 Unauthorized: Invalid credentials.
    """
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
    """
        API endpoint for updating user information.

        PUT:
        Update user information for the authenticated user.

        Authorization:
        Include the access token in the Authorization header as 'Bearer <access_token>'.

        Payload:
        {
            "name": "string required",
            "email": "string required",
            "address": "string required"
        }

        Returns:
        - If successful, returns updated user data.
        - If unsuccessful due to invalid data or missing/invalid token, returns error messages.

        Status Codes:
        - 200 OK: User updated successfully.
        - 400 Bad Request: Invalid data provided.
        - 401 Unauthorized: Invalid or missing token.
        """
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
    """
        API endpoint for deleting a user account.

        DELETE:
        Delete the authenticated user's account.

        Authorization:
        Include the access token in the Authorization header as 'Bearer <access_token>'.

        Returns:
        - If successful, returns a success message.
        - If unsuccessful due to authentication failure or other errors, returns error messages.

        Status Codes:
        - 204 No Content: User deleted successfully.
        - 401 Unauthorized: Invalid or missing token.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = UserDeletionSerializer(data={}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.delete()
        return Response({'message': 'User deleted successfully'})

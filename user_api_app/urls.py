from django.urls import path
from .views import UserRegistrationAPIView, TokenGenerationAPIView, DeleteUserView, UserUpdateAPIView


urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name="user-registration"),
    path('update/', UserUpdateAPIView.as_view(), name="user-update"),
    path("sign-in/", TokenGenerationAPIView.as_view(), name="user-sign-in"),
    path("delete/", DeleteUserView.as_view(), name="delete-user"),
]

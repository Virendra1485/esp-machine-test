from django.urls import path
from .views import BusinessRegistrationAPIView, BusinessListAPIView


urlpatterns = [
    path('registration/', BusinessRegistrationAPIView.as_view(), name="business-registration"),
    path('list/', BusinessListAPIView.as_view(), name="business-list"),
    # path('update/', UserUpdateAPIView.as_view(), name="user-update"),
    # path("sign-in/", TokenGenerationAPIView.as_view(), name="user-sign-in"),
]

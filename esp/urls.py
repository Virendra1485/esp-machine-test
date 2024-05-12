from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include("user_api_app.urls")),
    path('api/business/', include("business_api_app.urls")),
]

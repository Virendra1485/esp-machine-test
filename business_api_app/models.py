from django.db import models
from user_api_app.models import Keys


class Business(Keys):
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name

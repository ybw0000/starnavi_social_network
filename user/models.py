from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    last_request = models.DateTimeField(auto_now=False, auto_created=False, auto_now_add=False, db_default=now())

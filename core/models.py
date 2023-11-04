from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
'''
As a best practice we should create this at the begining of the project eventhough 
we don't need it, to allow the ease of customizition later
'''
class User(AbstractUser):
    email = models.EmailField(unique=True)
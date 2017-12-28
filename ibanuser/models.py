from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# changing the behaviour of email attribute of User model, making it unique
User._meta.get_field('email')._unique = True

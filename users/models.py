import datetime
import random
import string
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

TOKEN_CHARS = string.ascii_letters + string.digits

def generate_token():
    token = None
    while token is None:
        token = ''.join([random.choice(TOKEN_CHARS) for _ in range(25)])
        try:
            Token.objects.get(key=token)
            token = None
        except Token.DoesNotExist:
            pass
    return token

class User(AbstractUser):

    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name}'


class Token(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    @classmethod
    def create_token(self, user):
        key = generate_token()
        expires_at = datetime.datetime.now() + datetime.timedelta(days=settings.AUTH_TOKEN_EXPIRY_DAYS)
        token = Token.objects.create(user=user, key=key, expires_at=expires_at)
        return token

import datetime
from django.conf import settings
from rest_framework import serializers
from users import models

INVALID_CREDENTIALS_ERROR = 'Invalid Credentials'

class TokenSerializer(serializers.ModelSerializer):

    token = serializers.CharField(source='key')

    class Meta:
        model = models.Token
        fields = ('token', 'expires_at')


class LoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        validated_data = super().validate(data)
        phone_number = validated_data['phone_number']
        password = validated_data.get('password')
        try:
            user = models.User.objects.get(phone_number=phone_number)
            if password and not user.check_password(password):
                raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR)
            validated_data['user'] = user
        except models.User.DoesNotExist:
            raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR)

        return validated_data

    def save(self):
        user = self.validated_data['user']
        user.token_set.all().delete()
        token = models.Token.create_token(user)
        self.token = token
        return token, user


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = ('id', 'name', 'email', 'phone_number')


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'name', 'email', 'phone_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def validate_email(self, email):
        if models.User.objects.filter(email__iexact=email).exists():
            msg = _('This user already exists. Please sign in.')
            raise serializers.ValidationError(msg)
        return email

    def validate_phone_number(self, phone_number):
        if models.User.objects.filter(phone_number__iexact=phone_number).exists():
            msg = _('This user already exists. Please sign in.')
            raise serializers.ValidationError(msg)
        return phone_number

    def save(self):
        password = self.validated_data.pop('password', None)
        user = super().save()
        user.set_password(password)
        user.save()
        return user
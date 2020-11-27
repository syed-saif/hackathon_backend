from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from users import authentication, models, serializers

NOT_VERIFIED_ERROR = 'Please verify your account'


class LoginView(APIView):

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            token, user = serializer.save()
            user_data = serializers.UserProfileSerializer(instance=user).data
            return_data = serializers.TokenSerializer(instance=token).data
            return_data['user'] = user_data
            return Response(data=return_data)
        return Response(data=serializer.errors, status=400)

class LogoutView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.token_set.all().delete()
        return Response(data={'message': 'Success'}, status=200)

class ProfileView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserProfileSerializer(instance=request.user)
        return Response(data=serializer.data)

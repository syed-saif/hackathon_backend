from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from instance import models, serializers
from users import authentication
from users.models import User


def index(request):
    return render(request, 'index.html')


class HandWrittenDetectViewSet(ModelViewSet):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DetectHandWrittenSerializer

    def get_queryset(self):
        detect_handwrittens = models.DetecHandWritten.objects.filter(created_by=self.request.user)
        return detect_handwrittens
from django.urls import path
from rest_framework.routers import DefaultRouter
from instance import views

router = DefaultRouter()
router.register(r'api/v1/detect', views.HandWrittenDetectViewSet, basename='detect')

urlpatterns = [
    path('', views.index),
] + router.urls

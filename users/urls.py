from django.urls import path

from users import views

urlpatterns = [
    path('api/v1/login/', views.LoginView.as_view()),
    path('api/v1/logout/', views.LogoutView.as_view()),
    path('api/v1/profile/', views.ProfileView.as_view()),
]
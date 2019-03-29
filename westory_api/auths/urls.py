from django.contrib import admin
from django.urls import path, include
from .views import SignUpWithGoogle, SignIn
from rest_framework.authtoken import views

urlpatterns = [
    path('signUpWithGoogle', SignUpWithGoogle.as_view()),
    path('signIn', SignIn.as_view()),
    # path('api-token-auth/', views.obtain_auth_token),
]

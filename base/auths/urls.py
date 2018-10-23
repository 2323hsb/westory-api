from django.contrib import admin
from django.urls import path, include
from .views import SignUpWithGoogle, SignIn

urlpatterns = [
    path('signUpWithGoogle', SignUpWithGoogle.as_view()),
    path('signIn', SignIn.as_view()),
]

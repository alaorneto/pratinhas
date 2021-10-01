from django.urls import path
from rest_framework import routers
from .views import RegisterView

router = routers.DefaultRouter()

urlpatterns = [
    path('register', RegisterView.as_view()),
]

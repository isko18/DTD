from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.users.views import UserReisterAPI

router = DefaultRouter()
router.register(r'users', UserReisterAPI, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
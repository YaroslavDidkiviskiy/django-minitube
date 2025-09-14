from django.urls import path, include
from rest_framework import routers

app_name = "video"

router = routers.DefaultRouter()

urlpatterns = [
	path("", include(router.urls)),
]
from django.urls import path

from . import views

app_name = "utils"

urlpatterns = [path("health/", views.health, name="health")]

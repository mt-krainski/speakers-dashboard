from django.urls import path

from presentation_manager import views

app_name = "bistro"

urlpatterns = [
    path(
        "presentation_add/",
        views.presentation_edit_view,
        name="presentation_add",
    ),
    path(
        "presentation_edit/<uuid:uuid>",
        views.presentation_edit_view,
        name="presentation_edit",
    ),
]

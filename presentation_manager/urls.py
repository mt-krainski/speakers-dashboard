from django.urls import path

from presentation_manager import views

app_name = "bistro"

urlpatterns = [
    path(
        "presentation_edit_view/",
        views.presentation_edit_view,
        name="presentation_edit_view",
    )
]

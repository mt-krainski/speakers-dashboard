from django.urls import path

from presentation_manager import views
from presentation_manager.views import PresentationListView

app_name = "bistro"

urlpatterns = [
    path(
        "presentation_add/",
        views.presentation_edit_view,
        name="presentation-add",
    ),
    path(
        "presentation_edit/<uuid:uuid>",
        views.presentation_edit_view,
        name="presentation-edit",
    ),
    path(
        "presentation_list",
        PresentationListView.as_view(),
        name="presentation-list",
    ),
]

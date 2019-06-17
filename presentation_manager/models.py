from django.conf import settings
from django.db import models


PRESENTATION_DIR = "presentations"


class PresentationType(models.Model):
    name = models.CharField(
        max_length=200, help_text="Name of the presentation type."
    )
    duration = models.FloatField(
        help_text="Duration of a presentation of this type."
    )


class Presentation(models.Model):
    title = models.CharField(
        max_length=200, help_text="Title of this presentation"
    )
    type = models.ForeignKey(
        PresentationType, on_delete=models.SET_NULL, null=True, blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    file = models.FileField(upload_to=PRESENTATION_DIR)

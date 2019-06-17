from django.conf import settings
from django.db import models

from presentation_manager.choices import PRESENTATION_DIR
from presentation_manager.validators import validate_presentation_file


class PresentationType(models.Model):
    name = models.CharField(
        max_length=200, help_text="Name of the presentation type."
    )
    duration = models.FloatField(
        help_text="Duration of a presentation of this type [min.]."
    )

    def __str__(self):
        return f"{self.name} ({self.duration} min.)"


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
    file = models.FileField(
        upload_to=PRESENTATION_DIR,
        validators=[validate_presentation_file],
        null=True,
        blank=True,
    )

    def __str__(self):
        author = f"{self.author}"
        if (
            self.author.first_name is not None
            and self.author.last_name is not None
        ):
            author = f"{self.author.first_name} {self.author_last_name}"
        return f"[{self.type.name}] {self.title} by {author}"

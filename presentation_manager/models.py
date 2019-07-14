import uuid
from django.conf import settings
from django.db import models

from presentation_manager.choices import PRESENTATION_DIR
from presentation_manager.formats import formats


class PresentationType(models.Model):
    name = models.CharField(
        max_length=200, help_text="Name of the presentation type."
    )
    duration = models.DurationField(
        help_text="Duration of a presentation of this type."
    )

    def __str__(self):
        return f"{self.name} ({self.duration})"


class Presentation(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
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
        validators=[formats.validate_format],
        null=True,
        blank=True,
    )

    def get_author_display(self):
        author = f"{self.author}"
        if not (
            self.author.first_name is None or self.author.first_name == ""
        ) and not (
            self.author.last_name is None or self.author.last_name == ""
        ):
            author = f"{self.author.first_name} {self.author.last_name}"
        return author

    def __str__(self):
        author = self.get_author_display()
        presentation_type = self.type.name if self.type is not None else "-"
        return f"[{presentation_type}] '{self.title}' by {author}"

import uuid
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models

from presentation_manager.choices import PRESENTATION_DIR
from presentation_manager.formats import (
    formats,
    FORMATS_CHOICES,
    get_format_hash_from_file,
    FORMATS,
)


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
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
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
    format = models.CharField(
        max_length=32, choices=FORMATS_CHOICES, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.file is not None:
            self.format = get_format_hash_from_file(self.file)
        return super().save(*args, **kwargs)

    @property
    def format_class(self):
        if self.format is None:
            return None
        return FORMATS[self.format]

    @property
    def launch_command(self):
        if self.format is None:
            return None
        return FORMATS[self.format].get_command(self)

    @property
    def has_file(self):
        return bool(self.file)  # https://stackoverflow.com/a/8850547

    def clean(self):
        errors = {}
        if self.start_time is None and self.end_time is not None:
            errors[
                "start_time"
            ] = "This value can't be empty if End time is provided"

        if (
            self.start_time is not None
            and self.end_time is not None
            and self.end_time < self.start_time
        ):
            errors["start_time"] = "Start time has to be before end time."
            errors["end_time"] = "End time has to be after start time."

        if (
            self.end_time is None
            and self.start_time is not None
            and self.type is not None
        ):
            self.end_time = self.start_time + self.type.duration

        if errors:
            raise ValidationError(errors)

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

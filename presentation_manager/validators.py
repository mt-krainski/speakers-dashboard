from presentation_manager.choices import VALID_FILE_EXTENSIONS


def validate_presentation_file(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in VALID_FILE_EXTENSIONS:
        raise ValidationError("Unsupported file extension!")

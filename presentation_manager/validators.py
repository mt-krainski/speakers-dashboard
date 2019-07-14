from presentation_manager.choices import VALID_FILE_EXTENSIONS


# TODO (mkrainski): this is no longer necessary, remove after squashing
#  migrations.
def validate_presentation_file(value):
    """Validate against pdf format."""
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in VALID_FILE_EXTENSIONS:
        raise ValidationError("Unsupported file extension!")

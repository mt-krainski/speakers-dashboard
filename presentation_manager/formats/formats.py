from abc import ABCMeta, abstractmethod
from hashlib import md5

from django.conf import settings
from django.utils.timezone import localtime


def _get_hash(format_):
    if isinstance(format_, BasePresentationFormat):
        format_ = format_.__name__
    return md5(format_.__name__.encode()).hexdigest()


def get_format_hash_from_file(file):
    if file is None or file == "":
        return None

    from django.core.exceptions import ValidationError

    for cls in BasePresentationFormat.__subclasses__():
        try:
            cls.validate_presentation_file(file)
            return _get_hash(cls)
        except ValidationError:
            pass
    raise ValueError("Unsupported file extension!")


def validate_format(file):
    """This will try to validate the input file against all known formats.

    Format is known when it's implemented as a subclass of
    BasePresentationFormat below.
    """
    from django.core.exceptions import ValidationError

    for cls in BasePresentationFormat.__subclasses__():
        try:
            cls.validate_presentation_file(file)
            return
        except ValidationError:
            pass
    raise ValidationError("Unsupported file extension!")


class BasePresentationFormat(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def validate_presentation_file(cls, file):
        pass

    @classmethod
    @abstractmethod
    def get_command(cls, presentation):
        pass

    @classmethod
    @abstractmethod
    def get_name_display(cls):
        pass


class PdfPresentationFormat(BasePresentationFormat):

    _pdfpc_time_format = "%H:%M"
    _name = "PDF"
    _presentation_command = "pdfpc"
    _valid_file_extensions = [".pdf"]

    @classmethod
    def validate_presentation_file(cls, file):
        """Check if file has pdf extension."""
        import os
        from django.core.exceptions import ValidationError

        ext = os.path.splitext(file.name)[1]
        if not ext.lower() in cls._valid_file_extensions:
            raise ValidationError("Unsupported file extension!")

    @classmethod
    def get_command(cls, presentation):
        """Return a command to launch the presentation."""
        from ..models import Presentation

        if not isinstance(presentation, Presentation):
            return None
        command = [cls._presentation_command, presentation.file.path]
        if presentation.type.duration is not None:
            s = presentation.type.duration.seconds
            hours, remainder = divmod(s, 3600)
            minutes, _ = divmod(remainder, 60)
            duration_str = f"{60 * hours + minutes:02}"
            command += ["--duration", duration_str]

        if (
            presentation.start_time is not None
            and presentation.end_time is not None
        ):
            local_start_time = localtime(presentation.start_time)
            local_end_time = localtime(presentation.end_time)
            command += [
                "--start-time",
                local_start_time.strftime(cls._pdfpc_time_format),
                "--end-time",
                local_end_time.strftime(cls._pdfpc_time_format),
            ]

        if settings.PDFPC_SWITCH_SCREENS:
            command += ["--switch-screens"]

        return command

    @classmethod
    def get_name_display(cls):
        return cls._name

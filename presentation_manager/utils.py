import subprocess

from django.conf import settings


def launch_presentation(presentation):
    command = [settings.PRESENTATION_COMMAND, presentation.file.path]
    if presentation.type.duration is not None:
        s = presentation.type.duration.seconds
        hours, remainder = divmod(s, 3600)
        minutes, _ = divmod(remainder, 60)
        duration_str = f"{60*hours+minutes:02}"
        command += ["-d", duration_str]
    subprocess.call(command)

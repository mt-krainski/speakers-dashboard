import subprocess


def launch_presentation(presentation):
    command = presentation.launch_command
    subprocess.call(command)

from django.contrib import admin

from presentation_manager.models import Presentation, PresentationType

admin.site.register(Presentation)
admin.site.register(PresentationType)

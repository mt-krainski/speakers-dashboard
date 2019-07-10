from django.contrib import admin
from django.urls import reverse

from presentation_manager.models import Presentation, PresentationType
from utils.html_utils import render_link, render_button

admin.site.register(PresentationType)


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author_link",
        "type_name",
        "type_duration",
        "launch_button",
    )

    def author_link(self, obj):
        return render_link(
            reverse("admin:auth_user_change", args=(obj.author.pk,)),
            obj.get_author_display(),
        )

    author_link.short_description = "Author"
    author_link.admin_order_field = "author__username"

    def type_name(self, obj):
        return obj.type.name

    type_name.short_description = "Type"
    type_name.admin_order_field = "type__name"

    def type_duration(self, obj):
        return obj.type.duration

    type_duration.short_description = "Duration"
    type_duration.admin_order_field = "type__duration"

    def launch_button(self, obj):
        return render_button(
            reverse(
                "presentation-manager:launch-presentation", args=(obj.uuid,)
            ),
            "Launch",
            disabled=not bool(obj.file),  # https://stackoverflow.com/a/8850547
        )

    launch_button.short_description = ""

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
        "format",
        "type_duration",
        "start_time",
        "end_time",
        "has_file",
        "launch_button",
    )

    fields = (
        ("title", "author", "type"),
        ("file", "format"),
        ("start_time", "end_time"),
    )

    readonly_fields = ("format",)

    ordering = ("start_time",)

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

    def has_file(self, obj):
        return obj.has_file

    has_file.boolean = True
    has_file.short_description = "File"

    def launch_button(self, obj):
        return render_button(
            reverse(
                "presentation-manager:launch-presentation", args=(obj.uuid,)
            ),
            "Launch",
            disabled=not obj.has_file,
        )

    launch_button.short_description = ""

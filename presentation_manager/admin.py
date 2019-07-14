from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.db import transaction
from django.urls import reverse

from presentation_manager.models import Presentation, PresentationType
from utils.html_utils import render_link, render_button

admin.site.register(PresentationType)


@admin.register(Presentation)
class PresentationAdmin(SortableAdminMixin, admin.ModelAdmin):

    actions = ("reorder_by_start_time",)

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

    def reorder_by_start_time(self, reqest, queryset):
        queryset = queryset.order_by("start_time")
        current_order = list(queryset.values_list("order", flat=True))
        current_order_sorted = sorted(current_order)
        with transaction.atomic():
            for item in queryset.all():
                item.order = current_order_sorted.pop(0)
                item.save()

    reorder_by_start_time.short_description = (
        "Reorder selected presentations by their Start Time"
    )

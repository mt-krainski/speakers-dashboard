from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponse,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from presentation_manager.forms import PresentationForm
from presentation_manager.models import Presentation
from presentation_manager.utils import launch_presentation


@login_required
def presentation_edit_view(request, uuid=None):
    presentation = None
    if uuid:
        presentation = get_object_or_404(Presentation, uuid=uuid)
        if presentation.author != request.user:
            return HttpResponseForbidden()

    if request.method == "POST":

        form = PresentationForm(
            request.POST,
            request.FILES,
            user=request.user,
            instance=presentation,
        )

        if form.is_valid():
            form.save()

            if presentation is None:
                messages.add_message(
                    request, messages.INFO, "Presentation has been added!"
                )
            else:
                messages.add_message(
                    request, messages.INFO, "Presentation has been updated!"
                )

            return HttpResponseRedirect(
                reverse("presentation-manager:presentation-list")
            )

    else:
        form = PresentationForm(user=request.user, instance=presentation)
    return render(
        request,
        "presentation_manager/manage_presentation.html",
        {"form": form},
    )


@staff_member_required
def launch_presentation_view(request, uuid):
    if request.method != "GET":
        return HttpResponseForbidden()

    presentation = get_object_or_404(Presentation, uuid=uuid)

    launch_presentation(presentation)

    return HttpResponse(status="200")


@method_decorator(login_required, name="dispatch")
class PresentationListView(ListView):

    model = Presentation

    paginate_by = 100

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_change_permission"] = self.request.user.has_perm(
            "presentation_manager.change_presentation"
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs

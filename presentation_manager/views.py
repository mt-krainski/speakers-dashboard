from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from presentation_manager.forms import PresentationForm
from presentation_manager.models import Presentation


@login_required
def presentation_edit_view(request, uuid=None):
    presentation = None
    if uuid:
        presentation = get_object_or_404(Presentation, uuid=uuid)
        if presentation.author != request.user:
            return HttpResponseForbidden()

    if request.method == "POST":

        form = PresentationForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            form.save()

            messages.add_message(
                request, messages.INFO, f"Presentation has been added!"
            )

            return HttpResponseRedirect(reverse("home"))

    else:
        form = PresentationForm(user=request.user, instance=presentation)
    return render(
        request,
        "presentation_manager/manage_presentation.html",
        {"form": form},
    )

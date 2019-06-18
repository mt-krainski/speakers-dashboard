from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from presentation_manager.forms import PresentationForm


@login_required
def presentation_edit_view(request):
    if request.method == "POST":

        form = PresentationForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            form.save()

            messages.add_message(
                request, messages.INFO, f"Presentation has been added!"
            )

            return HttpResponseRedirect(reverse("home"))

    else:
        form = PresentationForm(user=request.user)
    return render(
        request,
        "presentation_manager/manage_presentation.html",
        {"form": form},
    )

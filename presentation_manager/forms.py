from django import forms
from django.apps import apps
from django.conf import settings

from presentation_manager.models import Presentation


class PresentationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        auth_model = apps.get_model(settings.AUTH_USER_MODEL)
        self.fields["author"] = forms.ModelChoiceField(
            widget=forms.HiddenInput(),
            queryset=auth_model.objects.filter(pk=user.pk),
            initial=user,
        )

    class Meta:
        model = Presentation
        fields = ["title", "type", "file", "author"]

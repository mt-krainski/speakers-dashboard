from django import forms

from presentation_manager.models import Presentation


class UploadPresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ["title", "file"]

from django import forms
from .models import Tugas


class KirimTugasForm(forms.Form):
    nim = forms.CharField()
    tugas = forms.ChoiceField(
        label="Tugas", choices=[(t.id, t.judul) for t in Tugas.objects.all()]
    )
    link_tugas = forms.URLField()

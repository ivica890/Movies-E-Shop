from django import forms

from hw5.models import Film


class MovieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control w-100"

    class Meta:
        model = Film
        exclude = ("trailer",)

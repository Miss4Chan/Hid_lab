# ne zaboravaj da importnesh forms od django
from django import forms
from .models import *
#Formata se kreira kako form model aka praime klasa za nejze
class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ##ova go praime za da im dodademe na site fields klasa od bootstrap za form control
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Post
        exclude = ('author',)

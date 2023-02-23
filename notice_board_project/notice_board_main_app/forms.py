from django.forms import ModelForm, CharField
from django.forms.widgets import CheckboxSelectMultiple

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, Response


class PostForm(ModelForm):
    text = CharField(widget=CKEditorUploadingWidget(), label='Текст')

    class Meta:
        model = Post
        fields = [
            'name',
            'text',
            'categories'
        ]
        widgets = {'categories': CheckboxSelectMultiple}
        labels = {
            'name': 'Назание',
            'categories': 'Категории'
        }


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = [
            'text'
        ]
        labels = {'text': 'Текст отклика'}

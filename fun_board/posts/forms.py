from django import forms
from .models import Posts


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'title',
            'category',
            'content',
        ]


class CommentCreateForm(forms.Form):
    content = forms.CharField(label="Отклик", widget=forms.Textarea)

    class Meta:
        fields = [
            'content',
        ]

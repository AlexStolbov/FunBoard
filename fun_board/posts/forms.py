from django import forms


class CommentCreateForm(forms.Form):
    content = forms.CharField(label="Отклик", widget=forms.Textarea)

    class Meta:
        fields = [
            'content',
        ]

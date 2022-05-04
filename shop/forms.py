from django import forms

from shop.models import Comment


class AddCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "content-control",
                                                           "placeholder": "Введите комментарий:"}))

    class Meta:
        model = Comment
        fields = ('content', )

from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.post = self.post
        comment.parent = self.parent
        if commit:
            comment.save()
        return comment

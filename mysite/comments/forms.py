from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Оставьте ваш комментарий...'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'text': 'Ваш комментарий',
            'rating': 'Оценка (1-5)'
        }
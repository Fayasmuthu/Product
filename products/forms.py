
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))

    class Meta:  # Corrected from 'class meta:'
        model = Review
        fields = ['name', 'email','review_title','rating', 'review_text']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name','class': 'spr-form-input spr-form-input-text', 'required': True}),
            'review_title':forms.TextInput(attrs={'placeholder':'Your Review Title'}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your Review'}),
        }

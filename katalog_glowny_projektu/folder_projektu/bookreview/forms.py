from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']  # Only include fields users can edit
        labels = {
            'rating': 'Rating (1-5)',
            'content': 'Review',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'content': forms.Textarea(attrs={'rows': 5}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Assuming you have a custom User model

class CustomUserCreationForm(UserCreationForm):
    # Add the fields you want to use in registration
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2', 'username']  # Include default fields too

    # Optional: You can add a clean method to add additional validation logic if needed
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")
        return email
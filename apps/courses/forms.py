from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'price', 'description', 'status', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul kursus'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan kategori kursus'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Deskripsi kursus...'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

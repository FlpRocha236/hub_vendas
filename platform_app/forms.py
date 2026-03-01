from django import forms
from .models import Course, Lesson, Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Seu Nome Completo', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Seu Melhor E-mail', 'class': 'form-control'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'thumbnail', 'slug']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'description', 'order']
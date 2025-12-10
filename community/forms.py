from django import forms
from .models import Resource, Topic, Post

# --- Resource Forms ---
class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = Resource
        # uploaded_by is set in the view
        fields = ['title', 'description', 'category', 'file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

# --- Discussion Forms ---
class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your reply...'}),
        }
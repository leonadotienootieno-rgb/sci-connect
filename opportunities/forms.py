from django import forms
from .models import JobPost
from .models import Application



class ApplicationStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Application

        fields = ['status']

class ApplicationForm(forms.ModelForm):
    cover_letter = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10}),
        required=False,
        label= "Cover Letter (Max 5000 characters)", max_length=5000,
    )
    class Meta:
        model = Application
        fields = ['cover_letter']

# class JobPostForm(forms.ModelForm):
#     class Meta:
#         model = JobPost
#         fields = ['title', 'description', 'category','location','is_internship','deadline']
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4 }),
#             'deadline': forms.DateInput(attrs={'deadline': 'date' }),
#         }


class JobPostCreateForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'requirements', 'location', 'category', 'job_type', 'is_active']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Senior Research Assistant'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description of the role...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                  'placeholder': 'Specific skills, degree level, experience...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country or Remote'}),
            'category': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'e.g., Biotechnology, Physics, IT'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class JobApplicationForm:
    def is_valid(self):
        pass

    def save(self, commit):
        pass
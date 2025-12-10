from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, StudentProfile, EmployerProfile


# --- Student Sign Up Form ---
class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    course = forms.CharField(max_length=100, required=True)
    university = forms.CharField(max_length=100, required=True)

    status = forms.ChoiceField(
        choices=StudentProfile.STATUS_CHOICES,
        label="Current Status",
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser

        # * CRITICAL FIX: Explicitly list all fields, excluding 'username' *
        fields = ('first_name', 'last_name', 'email', 'password2')


    def save(self, commit=True):
        # This save method needs to be robust, ensuring fields are passed correctly.
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        # Save StudentProfile data
        StudentProfile.objects.create(
            user=user,
            course=self.cleaned_data.get('course'),
            university=self.cleaned_data.get('university'),
            status=self.cleaned_data.get('status'),
        )
        return user


# --- Employer Sign Up Form ---
class EmployerSignUpForm(UserCreationForm):
    # These fields are for the EmployerProfile creation
    company_name = forms.CharField(max_length=255, required=True)
    industry = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser

        fields = ('email', 'password2')


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        user.save()

        EmployerProfile.objects.create(
            user=user,
            company_name=self.cleaned_data.get('company_name'),
            industry=self.cleaned_data.get('industry'),
        )
        return user


# --- Student Profile Update Form (NEW) ---
class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        # Fields the student can change or update
        fields = ['course', 'university', 'graduation_year', 'status', 'resume']

        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2024'}),
        }


class CustomUserEditForm(forms.ModelForm):
    # Ensure these fields are explicitly defined for editing
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    # Note: We intentionally exclude email and password, which should have separate change views

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


# Form for fields in the StudentProfile model
class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        # Expose all student-specific editable fields
        fields = ['course', 'university', 'status', 'graduation_year']

        # Add widget customization if needed, e.g., for Textarea or DateInput
        # widgets = {
        #     'graduation_year': forms.NumberInput(attrs={'placeholder': 'e.g., 2026'})
        # }
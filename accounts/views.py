from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from opportunities.models import Application, JobPost
from community.models import Resource
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from opportunities.views import is_employer
from .forms import StudentSignUpForm, EmployerSignUpForm, StudentProfileEditForm, CustomUserEditForm
from .models import EmployerProfile, StudentProfile


def is_student_check(user):
    return user.is_student
def is_student_user(user):
    return user.is_authenticated and user.is_student


@login_required
@user_passes_test(is_student_user, login_url='/')  # Redirects non-students away
def student_dashboard_view(request):
    # Get the student's profile
    student_profile = request.user.studentprofile
    applications = Application.objects.filter(applicant=student_profile).order_by('status', '-application_date')

    # Fetch a summary of application status
    summary = {
        'total_applied': applications.count(),
        # Assuming 'I' is Interview and 'H' is Hired status key from Application.STATUS_CHOICES
        'interviews': applications.filter(status='I').count(),
        'hired': applications.filter(status='H').count(),
    }
    recommended_resources = Resource.objects.all().order_by('-uploaded_at')[:5]

    context = {
        'student_profile': student_profile,
        'applications': applications,
        'summary': summary,
        'recommended_resources': recommended_resources,
    }
    return render(request, 'student_dashboard.html', context)
# --- SIGNUP VIEWS ---
def student_signup_view(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log in the new user
            return redirect('dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'student_signup.html', {'form': form})

def employer_signup_view(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('employer_dashboard') # Redirect to employer specific dashboard
    else:
        form = EmployerSignUpForm()
    return render(request, 'employer_signup.html', {'form': form})

# --- LOGIN VIEW ---
class CustomLoginView(LoginView):
    template_name = 'login.html'
    # Success URL is set in settings.py: LOGIN_REDIRECT_URL = '/' (or a custom path)

def student_profile_update(request):
    return None

def is_student(user):
    return user.is_authenticated and user.is_student

@login_required
@user_passes_test(is_student)
def student_dashboard_view(request):
    # 1. Fetch the student's profile data
    try:
        student_profile = request.user.studentprofile
    except Exception:
        # Handle case where profile might not exist immediately after signup
        student_profile = None

    # 2. Fetch all applications submitted by the current user (Student)
    applications = Application.objects.filter(applicant=student_profile).order_by('-applied_at')

    context = {
        'student_profile': student_profile,
        'applications': applications,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
@user_passes_test(is_employer)
def employer_dashboard_view(request):
    try:
        employer_profile = request.user.employerprofile
        JobPost.objects.filter(employer=employer_profile).order_by('-posted_at')
    except EmployerProfile.DoesNotExist:
        job_posts = []
        applications = []
    context = {
        'job_posts': job_posts,
        'applications': applications,
    }
    return render(request, 'employer_dashboard.html', context)


def is_student(user):
    return user.is_authenticated and user.is_student


@login_required
@user_passes_test(is_student)
def student_profile_edit_view(request):
    # Get the user instance and the related student profile instance
    user = request.user
    # Ensure profile exists, creating it if necessary (though it should exist after signup)
    student_profile, created = StudentProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # 1. Initialize forms with POST data and current instances
        user_form = CustomUserEditForm(request.POST, instance=user)
        profile_form = StudentProfileEditForm(request.POST, instance=student_profile)

        if user_form.is_valid() and profile_form.is_valid():
            # 2. Save both forms
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile was updated successfully!')
            # 3. Redirect back to the dashboard
            return redirect(reverse('student_dashboard'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # 1. Initialize forms with current instance data (GET request)
        user_form = CustomUserEditForm(instance=user)
        profile_form = StudentProfileEditForm(instance=student_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'student_profile': student_profile,
    }
    return render(request, 'student_profile_edit.html', context)
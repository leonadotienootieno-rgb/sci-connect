from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from opportunities.models import Application, JobPost
from community.models import Resource
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import StudentSignUpForm, EmployerSignUpForm


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

    # 3. Recommend resources based on student's course/university
    # For MVP, just fetch the most recent resources
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
            return redirect('dashboard') # Redirect to a generic dashboard or profile setup
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
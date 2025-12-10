from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.urls import reverse
from django.db.models import Q
from django.template.context_processors import request
from .models import JobPost, Application
from .forms import ApplicationForm,JobPostCreateForm, ApplicationStatusUpdateForm, JobApplicationForm
from .models import JOB_CATEGORIES,JOB_LOCATIONS

def is_student(user):
    return user.is_authenticated and user.is_student


@login_required
@user_passes_test(is_student, login_url='/accounts/login/')
def job_apply_view(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)
    student_profile = request.user.studentprofile  # Assuming profile exists

    # 1. Check if the student has already applied
    if Application.objects.filter(applicant=student_profile, job=job).exists():
        messages.warning(request, f"You have already applied for the job: {job.title}.")
        return redirect(reverse('job_detail_view', args=[job_id]))

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            # Create the application object but don't save to DB yet
            application = form.save(commit=False)

            # Manually assign the FKs (Foreign Keys)
            application.job = job
            application.applicant = student_profile

            # NOTE: application_date is set via auto_now_add in the model.
            application.save()

            messages.success(request, f"Successfully applied for the job: {job.title}!")
            # Redirect to the student's dashboard to see the application tracking
            return redirect(reverse('student_dashboard'))
    else:
        form = JobApplicationForm()

    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'job_apply.html', context)
def job_list_view(request):
    jobs = JobPost.objects.filter(is_active=True ).order_by('-posted_at')
    search_query = request.GET.get('q')
    selected_category = request.GET.get('location')
    if search_query:
        jobs = jobs.filter(Q(title__icontains=search_query)|Q(description__icontains=search_query)|Q(requirements__icontains=search_query)
                           |Q(employer_company_name__icontains=search_query)).distinct()
    if selected_category and selected_category != 'all' :
        jobs = jobs.filter(category=selected_category)
    if location_filter and location_filter != 'all' :
        jobs = jobs.filter(location=location_filter)

    context = {
        'jobs': jobs,
        'search_query': search_query,
        'selected_category': selected_category,
        'location_filter': location_filter,
    }
    return render(request, 'job_list.html', context)

@login_required
def job_apply_view(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)

    # Check 1: Ensure user is a student/job-seeker type
    if not request.user.is_student:
        messages.error(request, "Only job-seeking users are authorized to apply for jobs.")
        return redirect('job_detail', job_id=job_id)

    applicant_profile = request.user.studentprofile  # Get the student's profile
    job_type = job.job_type
    applicant_status = applicant_profile.status

    if job_type == 'attachment' and applicant_status != 'student':
        messages.error(request,
                       "This is a course-credit Attachment, reserved only for Current Students.")
        return redirect('job_detail', job_id=job_id)

    # Rule 2: Internships/Jobs are ONLY for Awaiting or Graduate status
    if (job_type == 'internship' or job_type == 'full_time') and applicant_status == 'student':
        messages.error(request,
                       "This opportunity is intended for Graduates and those Awaiting Graduation.")
        return redirect('job_detail', job_id=job_id)

    # Check 3: Check for Duplicate Application
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', job_id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, f"Successfully applied for '{job.title}'!")
            return redirect('student_dashboard')
    else:
        form = ApplicationForm()

    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'job_apply.html', context)


@login_required
def student_dashboard_view(request):
    # Security Check: Only students should access this dashboard
    if not request.user.is_student:
        return redirect('home')

    # Fetch all applications submitted by the logged-in user
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')

    context = {
        'applications': applications,
        'student_profile': request.user.studentprofile
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def employer_dashboard_view(request):
    # Security Check: Only employers should access this dashboard
    if not request.user.is_employer:
        messages.error(request, "Access denied. Only employers can view this dashboard.")
        return redirect('home')

    # Get the EmployerProfile instance
    employer_profile = request.user.employerprofile

    # Fetch all jobs posted by this employer and annotate with the count of applications
    job_posts = JobPost.objects.filter(employer=employer_profile).annotate(
        application_count=Count('application')
    ).order_by('-posted_at')

    context = {
        'employer_profile': employer_profile,
        'job_posts': job_posts
    }

    return render(request, 'employer_dashboard.html', context)

@login_required
def job_create_view(request):
    # 1. Security Check: Only employers can post jobs
    if not request.user.is_employer:
        messages.error(request, "Access denied. Only employers can create job listings.")
        return redirect('home')

    if request.method == 'POST':
        form = JobPostCreateForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            # Set the employer field automatically
            job_post.employer = request.user.employerprofile
            job_post.save()
            messages.success(request, f"Job Post '{job_post.title}' created successfully!")
            return redirect('employer_dashboard')
    else:
        form = JobPostCreateForm()

    context = {
        'form': form
    }
    return render(request, 'job_create.html', context)


@login_required
def application_list_view(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)

    if not request.user.is_employer or job.employer != request.user.employerprofile:
        messages.error(request, "Access denied. You are not authorized to view these applications.")
        return redirect('employer_dashboard')

    applications = Application.objects.filter(job=job).order_by('-applied_at')

    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'application_list.html', context)


def job_detail_view(request, job_id):
    """
    Displays the details of a single job post.
    """
    # Fetches the job post or raises a 404 error if not found
    job = get_object_or_404(JobPost, pk=job_id)

    context = {
        'job': job
    }
    return render(request, 'job_detail.html', context)

def is_employer(user):
    return user.is_authenticated and user.is_employer

@login_required
@user_passes_test(is_employer)
def application_status_update(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if application.job.employer.user != request.user:
        return render(request,'403.html', status=403)

    if request.method == 'POST':
        form = ApplicationStatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect(reverse('employer_dashboard'))
        else:
            form = ApplicationStatusUpdateForm(instance=application)
            context = {
                'form': form,
                'application': application,
            }
            return render(request, 'application_status_update.html')


@login_required
@user_passes_test(is_employer)
def application_detail_view(request, application_id):
    """
    Allows employer to view full application details and update the status.
    """
    application = get_object_or_404(Application, pk=application_id)

    # CRITICAL Security check: Ensure the current employer owns the job post
    if application.job.employer.user != request.user:
        # If the employer doesn't own the job, return Forbidden
        return render(request, '403.html', status=403)

        # We reuse the status update form logic here
    if request.method == 'POST':
        form = ApplicationStatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            # Use Django's messages framework for feedback
            from django.contrib import messages
            messages.success(request,
                             f"Status for {application.applicant.get_full_name}'s application updated successfully!")
            return redirect(reverse('employer_dashboard'))
    else:
        form = ApplicationStatusUpdateForm(instance=application)

    context = {
        'application': application,
        'student_profile': application.applicant,  # Direct access to the student profile
        'form': form,
    }
    return render(request, 'application_detail.html', context)

def job_detail_view(request, job_id):
    """Displays the details of a single job post."""
    # Fetches the job post or raises a 404 error if not found
    job = get_object_or_404(JobPost, pk=job_id)

    context = {
        'job': job,
    }
    return render(request, 'job_detail.html', context)
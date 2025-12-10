from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.template.context_processors import request

from .models import JobPost, Application
from .forms import ApplicationForm,JobPostCreateForm


def job_list_view(request):
    jobs = JobPost.objects.all().order_by('-posted_at')
    context = {
        'jobs': jobs,
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
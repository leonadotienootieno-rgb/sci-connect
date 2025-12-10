from django.db import models
from accounts.models import EmployerProfile, CustomUser

# --- JobPost Model ---
class JobPost(models.Model):
    # Job Type Choices (for eligibility logic)
    TYPE_CHOICES = (
        ('attachment', 'Attachment (Student Credit)'),
        ('internship', 'Internship'),
        ('full_time', 'Full-Time Job'),
    )

    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Job Type field (Fixes OperationalError: job_type)
    job_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='full_time'
    )

    category = models.CharField(max_length=50, default='Science')

    def _str_(self):
        return self.title


# --- Application Model ---
class Application(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    # The applicant is the CustomUser who applied
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'), ('reviewed', 'Reviewed'), ('rejected', 'Rejected')),
        default='pending'
    )
    cover_letter_snippet = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def _str_(self):
        return f"Application for {self.job.title} by {self.applicant.email}"

JOB_CATEGORIES = (
    ('CS', 'Computer Science (Software, Data, AI)'),
    # ... (rest of your categories) ...
)

JOB_LOCATIONS = (
    ('Nairobi', 'Nairobi'),
    ('Remote', 'Remote'),
    # ... (rest of your locations) ...
)

class JobPost(models.Model):
    # ... your model fields ...
    category = models.CharField(max_length=50, choices=JOB_CATEGORIES)
    # ...
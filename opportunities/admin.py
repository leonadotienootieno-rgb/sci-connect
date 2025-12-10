from django.contrib import admin
from .models import JobPost, Application


# --- JobPost Admin Configuration ---
class JobPostAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'employer', 'job_type', 'is_active', 'posted_at')

    # Fields to filter the list by
    list_filter = ('is_active', 'job_type', 'posted_at', 'employer')

    # Fields to search against
    search_fields = ('title', 'description', 'requirements', 'location')



# --- Application Admin Configuration ---
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')

    list_filter = ('status', 'applied_at', 'job')

    # Fields to search against
    search_fields = ('job_title', 'applicant_email', 'cover_letter_snippet')

    ordering = ('-applied_at',)

admin.site.register(JobPost, JobPostAdmin)
admin.site.register(Application, ApplicationAdmin)
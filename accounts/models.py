from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


# --- Custom User Manager (Placeholder - use your actual implementation) ---
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# --- CustomUser Model ---
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_student = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)


    objects = CustomUserManager()

    def _str_(self):
        return self.email

class StudentProfile(models.Model):
    # Status Choices for eligibility logic
    STATUS_CHOICES = (
        ('student', 'Current Student (Seeking Attachments)'),
        ('awaiting', 'Awaiting Graduation (Seeking Internships/Jobs)'),
        ('graduate', 'Graduate (Seeking Internships/Jobs)'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    course = models.CharField(max_length=100)
    university = models.CharField(max_length=100)

    # Field causing previous errors (Ensure this is present)
    graduation_year = models.IntegerField(null=True, blank=True)

    # New status field for eligibility
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='student'
    )

    # Resume field for file upload (Fixes FieldError: resume)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def _str_(self):
        return self.user.get_full_name()


# --- EmployerProfile Model ---
class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)

    def _str_(self):
        return self.company_name
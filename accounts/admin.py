from django.contrib import admin
from .models import CustomUser, StudentProfile, EmployerProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # What fields to display in the list view
    list_display = ('email', 'username', 'is_student', 'is_employer', 'is_active', 'is_staff', 'date_joined')

    list_filter = ('is_student', 'is_employer', 'is_staff', 'is_active')

    search_fields = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Roles', {'fields': ('is_student', 'is_employer')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = ('user_email', 'university', 'course', 'graduation_year')
    search_fields = ('user_email', 'user_username', 'university', 'course')
    list_filter = ('graduation_year',)


    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):

    list_display = ('user_email', 'company_name', 'industry', 'contact_phone')
    search_fields = ('user__email', 'company_name', 'industry')
    list_filter = ('industry',)

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'

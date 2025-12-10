from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import student_signup_view, employer_signup_view, CustomLoginView, student_dashboard_view,student_profile_update #profile_edit_view #for future use

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/student/', student_signup_view, name='student_signup'),
    path('signup/employer/', employer_signup_view, name='employer_signup'),
    path('dashboard/', student_dashboard_view, name='student_dashboard'),
    path('profile/update', student_profile_update, name='student_profile_update'),
    # path('profile/edit/', profile_edit_view, name='profile_edit')
]
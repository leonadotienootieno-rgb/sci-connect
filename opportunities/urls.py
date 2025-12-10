from django.shortcuts import render
from django.urls import path
from .views import (
    job_list_view,
    job_create_view,
    job_apply_view,
    employer_dashboard_view,
    application_list_view,
    job_detail_view,
    student_dashboard_view, application_status_update)
from . import view
from opportunities import views

urlpatterns = [
    path('',job_apply_view ,name='job_list'),
    path('apply/<int:job_id>/',job_apply_view,name='job_apply'),
    path('post/', job_create_view, name='job_create'),
    path('jobs/', job_list_view, name='job_list'),
    path('dashboard/', employer_dashboard_view, name='employer_dashboard'),
    path('applicants/<int:job_id>/', application_list_view, name='application_list'),
    path('jobs/<int:job_id>/', job_detail_view, name='job_detail_view'),
    path('jobs/<int:job_id>/apply/', view.job_apply_view, name='job_apply'),
    path('dashboard/student/', student_dashboard_view, name='student_dashboard'),
    path('dashboard/employer/', employer_dashboard_view, name='employer_dashboard'),
    path('jobs/create/', job_create_view, name='job_create'),
    path('jobs/<int:job_id>/applicants/',application_list_view , name='application_list'),



]
from django.urls import path
from .views import JobListView, JobDetailView, JobCreateView
from django.contrib.auth import views as auth_views
from .views import register
from . import views
urlpatterns = [
    path('', JobListView.as_view(), name='job_list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('create/', JobCreateView.as_view(), name='job_create'),
    
    #auth

    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='job_list'), name='logout'),
    path('approve-recruiters/', views.pending_recruiters, name='pending_recruiters'),
    path('approve-recruiter/<int:user_id>/', views.approve_recruiter, name='approve_recruiter'),
]

# jobs/urls.py
from django.urls import path
from . import views
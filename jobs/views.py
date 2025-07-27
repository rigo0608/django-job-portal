from .models import JobPost
from .forms import JobPostForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.core.mail import send_mail


from django.views.generic import ListView
from django.db.models import Q
from .models import JobPost

class JobListView(ListView):
    model = JobPost
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return JobPost.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by('-posted_at')  # Ensure consistent pagination
        return JobPost.objects.all().order_by('-posted_at')  # Order by latest first



class JobDetailView(DetailView):
    model = JobPost
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'




class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        user = self.request.user
        # Allow if user is staff
        if user.is_staff:
            return True
        # Allow if user has a profile and is an approved recruiter
        try:
            return user.userprofile.is_recruiter and user.userprofile.is_approved
        except UserProfile.DoesNotExist:
            return False



from .models import UserProfile  # import your profile model

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Safe update (profile already created via signal)
            is_recruiter = request.POST.get('is_recruiter') == 'on'
            user.userprofile.is_recruiter = is_recruiter
            user.userprofile.save()

            messages.success(request, '✅ Account created! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# jobs/views.py
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def pending_recruiters(request):
    recruiters = UserProfile.objects.filter(is_recruiter=True, is_approved=False)
    return render(request, 'jobs/pending_recruiters.html', {'recruiters': recruiters})

from django.shortcuts import get_object_or_404

@user_passes_test(lambda u: u.is_staff)
@user_passes_test(lambda u: u.is_staff)
def approve_recruiter(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)
    profile.is_approved = True
    profile.save()

    # ✅ Send approval email
    send_mail(
        subject='✅ Your Recruiter Account Has Been Approved',
        message=f'Dear {profile.user.username},\n\nCongratulations! Your recruiter profile is now approved. You can now post jobs on our platform.',
        from_email='ritikgoel0608@gmail.com',  # Replace with your actual admin email
        recipient_list=[profile.user.email,
            'ritikgoel0608@gmail.com'],
        
        fail_silently=True,
    )

    messages.success(request, f"✅ {profile.user.username} has been approved as a recruiter.")
    return redirect('pending_recruiters')




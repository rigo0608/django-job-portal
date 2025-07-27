from django.contrib import admin
from .models import JobPost
from .models import UserProfile


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_at')



from django.contrib import admin
from django.core.mail import send_mail
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_recruiter', 'is_approved')
    list_filter = ('is_recruiter', 'is_approved')
    search_fields = ('user__username', 'user__email')
    actions = ['approve_recruiters']

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = UserProfile.objects.get(pk=obj.pk)
            if not old_obj.is_approved and obj.is_approved:
                # Send approval email
                send_mail(
                    subject='✅ Recruiter Profile Approved',
                    message=f'Dear {obj.user.username},\n\nYour recruiter account has been approved. You can now post jobs on the portal.',
                    from_email='admin@yourdomain.com',  # replace with actual email
                    recipient_list=[obj.user.email],
                    fail_silently=True,
                )
        super().save_model(request, obj, form, change)

    def approve_recruiters(self, request, queryset):
        updated_count = 0
        for obj in queryset:
            if not obj.is_approved:
                obj.is_approved = True
                obj.save()
                updated_count += 1
        self.message_user(request, f"{updated_count} recruiter(s) approved and notified.")
    
    approve_recruiters.short_description = "Approve selected recruiters and send email"




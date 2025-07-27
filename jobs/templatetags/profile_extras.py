from django import template

register = template.Library()

@register.filter(name='can_post_job')
def can_post_job(user):
    if not user.is_authenticated:
        return False

    # Staff users can always post jobs
    if user.is_staff:
        return True

    # Try to get userprofile, return False if not present
    profile = getattr(user, 'userprofile', None)
    if profile and profile.is_recruiter and profile.is_approved:
        return True

    return False

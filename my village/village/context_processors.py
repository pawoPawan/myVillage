from .models import RelationshipRequest

def pending_requests(request):
    """Add pending relationship requests count to the template context."""
    if request.user.is_authenticated:
        pending_count = RelationshipRequest.objects.filter(
            to_user=request.user.userprofile,
            status='pending'
        ).count()
        return {'pending_requests_count': pending_count}
    return {'pending_requests_count': 0} 
from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        unread = request.user.notifications.filter(is_read=False)
        return {
            'unread_notifications': unread,
            'unread_count': unread.count(),
            'recent_notifications': request.user.notifications.all().order_by('-created_at')[:5],
        }
    return {}

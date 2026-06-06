from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Notification
from hostels.models import Hostel
from users.models import CustomUser


def notify_all_admins(message):
    admins = CustomUser.objects.filter(role='admin')
    for admin in admins:
        Notification.objects.create(user=admin, message=message)


@receiver(post_save, sender=Booking)
def booking_notification(sender, instance, created, **kwargs):
    if created:
        # Notify owner of new booking request
        Notification.objects.create(
            user=instance.hostel.owner,
            message=f'{instance.student.username} requested to book "{instance.hostel.name}".'
        )
    else:
        if instance.status == 'approved':
            Notification.objects.create(
                user=instance.student,
                message=f'Your booking for "{instance.hostel.name}" has been approved! 🎉'
            )
        elif instance.status == 'rejected':
            Notification.objects.create(
                user=instance.student,
                message=f'Your booking for "{instance.hostel.name}" was rejected.'
            )


@receiver(post_save, sender=Hostel)
def hostel_notification(sender, instance, created, **kwargs):
    if created:
        # Notify all admins of new hostel submission
        notify_all_admins(
            f'New hostel "{instance.name}" submitted by {instance.owner.username} — needs approval.'
        )
    else:
        if instance.status == 'approved':
            # Notify owner
            Notification.objects.create(
                user=instance.owner,
                message=f'Your hostel "{instance.name}" has been approved! 🎉 It is now live.'
            )
            # Notify all admins
            notify_all_admins(f'Hostel "{instance.name}" has been approved.')

        elif instance.status == 'rejected':
            # Notify owner
            Notification.objects.create(
                user=instance.owner,
                message=f'Your hostel "{instance.name}" was rejected by admin.'
            )


@receiver(post_save, sender=CustomUser)
def new_owner_notification(sender, instance, created, **kwargs):
    if created and instance.role == 'owner':
        notify_all_admins(
            f'New hostel owner "{instance.username}" just registered.'
        )

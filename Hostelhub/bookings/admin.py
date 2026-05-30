
from django.contrib import admin
from .models import Booking, SavedHostel


class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'hostel', 'status',
                    'move_in_date', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__username', 'hostel__name')


class SavedHostelAdmin(admin.ModelAdmin):
    list_display = ('student', 'hostel', 'saved_at')


admin.site.register(Booking, BookingAdmin)
admin.site.register(SavedHostel, SavedHostelAdmin)

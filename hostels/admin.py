# hostels/admin.py
from django.contrib import admin
from .models import Hostel, HostelImage


class HostelImageInline(admin.TabularInline):
    model = HostelImage
    extra = 1


class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'hostel_type',
                    'price_per_month', 'status', 'available_rooms')
    list_filter = ('status', 'hostel_type', 'city')
    search_fields = ('name', 'city', 'owner__username')
    inlines = [HostelImageInline]


class HostelImageAdmin(admin.ModelAdmin):
    list_display = ('hostel', 'is_primary', 'uploaded_at')


admin.site.register(Hostel, HostelAdmin)
admin.site.register(HostelImage, HostelImageAdmin)

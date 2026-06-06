# hostels/forms.py

from django import forms
from .models import Hostel, HostelImage, Review


class HostelForm(forms.ModelForm):
    admission_fee = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 2000 (leave blank if none)',
        })
    )

    class Meta:
        model = Hostel
        fields = [
            # Basic info
            'name', 'city', 'address', 'description',
            'hostel_type', 'room_type', 'price_per_month',
            'total_rooms', 'available_rooms', 'admission_fee',
            'contact_number',
            # Amenities
            'has_wifi', 'has_parking', 'has_laundry',
            'has_hot_water', 'has_cctv', 'has_kitchen',
            'has_meals', 'has_study_room', 'has_power_backup',
            # Extra info
            'nearby_landmarks', 'minimum_stay', 'hostel_rules',
            # Location
            'latitude', 'longitude',
            # Availability
            'is_available',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Sunrise Hostel',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Kathmandu',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Baneshwor, Kathmandu',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your hostel...',
            }),
            'hostel_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'room_type': forms.RadioSelect(),
            'price_per_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 4500',
            }),
            'total_rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 20',
            }),
            'available_rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 5',
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 9841234567',
            }),
            # Amenities — existing
            'has_wifi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_laundry': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_hot_water': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_cctv': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_kitchen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # Amenities — new
            'has_meals': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_study_room': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_power_backup': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # Extra info
            'nearby_landmarks': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Near Tribhuvan University, 5 min from bus stop',
            }),
            'minimum_stay': forms.Select(attrs={
                'class': 'form-select',
            }),
            'hostel_rules': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g. No smoking, no guests after 9pm, no loud music...',
            }),
            # Location
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 27.7172',
                'step': 'any',
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 85.3240',
                'step': 'any',
            }),
            # Availability
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HostelImageForm(forms.ModelForm):
    class Meta:
        model = HostelImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# class MultipleImageForm(forms.Form):
#     """Use this for uploading multiple images at once."""
#     images = forms.FileField(
#         widget=forms.FileInput(attrs={
#             'class': 'form-control',
#             'multiple': True,
#         }),
#         required=False,
#     )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'star-rating-input'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience at this hostel...',
            }),
        }

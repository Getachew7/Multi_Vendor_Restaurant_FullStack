from account.validator import allow_only_images_validator
from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    vendor_licence = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_licence']
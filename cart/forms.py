from django import forms
from user_account.models import *



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["name", "house_name", "address_line_1", "city", "state", "country", "phone", "pincode"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'house_name': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'city': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'state': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'country': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            
        }


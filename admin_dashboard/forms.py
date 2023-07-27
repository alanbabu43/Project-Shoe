from django import forms
#from . models import Amodel
from user_account . models import *
from products.models import *
from multiupload.fields import MultiFileField, MultiMediaField
from order.models import *


class Aforms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields=['email','name','password']
        widgets={
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(render_value=True,attrs={'class':'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=['category_name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields=['brand_name']

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields=['name']

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields=['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "Brand","Category", "stock", "discription", "price", "gender", "image", "is_available"]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'Brand': forms.Select(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'discription': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'})
            # 'image': forms.ClearableFileInput(attrs={'multiple': True}),
            
        }
    image = forms.ImageField(label='Product Image', required=True, error_messages={'required': 'Please upload an image.'})

class VariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product_name', 'color', 'size', 'stock', 'price']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product_name','image']


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'is_expired', 'discount_price', 'minimum_amount']
        widgets = {
            'coupon_code': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            # 'is_expired': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'is_expired': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'minimum_amount': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'}),
            
        }

class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
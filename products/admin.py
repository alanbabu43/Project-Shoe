from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductVariant)
admin.site.register(Color)
admin.site.register(Size)


class ProductImageAdmin(admin.StackedInline):
    model =ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Wishlist)
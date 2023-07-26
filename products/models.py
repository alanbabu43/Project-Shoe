from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique = True)
    slug = AutoSlugField(populate_from='category_name',unique=True,null=True,default=None)
    # description = models.TextField(max_length=255)
    # category_image = models.ImageField(upload_to='images' , blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.category_name)
    #     super().save(*args, **kwargs)    

    # def get_absolute_url(self):
    #     return reverse('product_by_category', args=[self.slug])    

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=200,unique=True)
    slug = AutoSlugField(populate_from='brand_name',unique=True,null=True,default=None)
    # Category = models.ForeignKey(Category,on_delete=models.CASCADE)


    def __str__(self):
        return self.brand_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = AutoSlugField(populate_from='product_name',unique=True,null=True,default=None)
    discription  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    stock        = models.IntegerField(default=0)
    gender       = models.CharField(max_length=100)
    image        = models.ImageField(upload_to='images/products/')
    is_available  =models.BooleanField(default=True)
    Category      =models.ForeignKey(Category,on_delete=models.CASCADE)
    Brand         =models.ForeignKey(Brand,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['Brand'].queryset = Brand.objects.all()
    #     self.fields['Category'].queryset = Category.objects.all()
    
    

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.product_name)
    #         i = 1
    #         while product.objects.filter(slug=self.slug).exists():
    #             self.slug = f"{slugify(self.product_name)}-{i}"
    #             i += 1
    #     super().save(*args, **kwargs)

    # def get_url(self):
    #     return reverse('product_details',args=[self.category.slug, self.slug])
    

#     def get_image_upload_path(instance, filename):
#         # Generate a unique filename for each uploaded image
#         return 'images/products/{0}/{1}'.format(instance.slug, filename)

#     image = models.ImageField(upload_to=get_image_upload_path)


#     # existing methods...


class Color(models.Model):
    name=models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.name
    
class Size(models.Model):
    name=models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class ProductVariant(models.Model):
    # color = models.CharField(max_length=200)
    # slug = AutoSlugField(populate_from='color',unique=True,null=True,default=None)
    # size = models.IntegerField()
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE,related_name="product_variant")
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # product_name = models.ForeignKey(Product,on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('product_name', 'size', 'color')
    
    def __str__(self) -> str:
        return self.color.name+':'+self.size.name

class ProductImage(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to='images/products/', blank=True)

    def __str__(self):
        return self.image.url


User = get_user_model()
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)







# class ProductVariant(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="productvariant")
#     size = models.ForeignKey(Size, on_delete=models.CASCADE)
#     # color = models.ForeignKey(Color, on_delete=models.CASCADE)
#     # color_image = models.ImageField(upload_to='product_images/')
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     stock = models.PositiveIntegerField(default=0)

#     def _str_(self):
#         return f"{self.product.name} - Size: {self.size.name}"

# class ProductColor(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="productcolor")
#     color = models.ForeignKey(Color, on_delete=models.CASCADE)
#     color_image = models.ImageField(upload_to='product_images/') 
    
#     def _str_(self):
#         return f"{self.product.name} -  Color: {self.color.name}"
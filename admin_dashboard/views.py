from django.shortcuts import get_object_or_404
from multiupload.fields import MultiFileField
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseRedirect
from user_account . models import  CustomUser
from . forms import *
from products . models import Product, Brand, Category, ProductVariant, Color, Size, ProductImage
from django.forms import formset_factory
from django.forms import inlineformset_factory
from order.models import *
from django.db.models import Q
import json
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractYear
from django.db.models import Count
import calendar
from datetime import date
from PIL import Image


 
# Create your views here.


# To add multiple images 
ImageFormSet = ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=5)


# admin home page
# @login_required(login_url='admin_login')
# def admin_panel(request):
#     today = date.today()

#     delivered_orders = Order.objects.filter(status='Delivered')
#     # delivered_orders = Order.objects.filter(status='Delivered')
#     delivered_orders_by_months = delivered_orders.annotate(delivered_month=ExtractMonth('created_at')).values('delivered_month').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_count')
#     print( delivered_orders_by_months)
#     delivered_orders_month = []
#     delivered_orders_number = []
#     for d in delivered_orders_by_months:
#         delivered_orders_month.append(calendar.month_name[d['delivered_month']])
#         delivered_orders_number.append(list(d.values())[1])


#     order_by_months = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
#     print(order_by_months)
#     monthNumber = []
#     totalOrders = []
#     for o in order_by_months:
#          monthNumber.append(calendar.month_name[o['month']])
#          totalOrders.append(list(o.values())[1])
#     print('ggggg',delivered_orders_number)
#     print(monthNumber)
#     print(totalOrders)
    
#     context ={
#          'delivered_orders':delivered_orders,
#          'order_by_months':order_by_months,
#          'monthNumber':monthNumber,
#          'totalOrders':totalOrders,
#          'delivered_orders_number':delivered_orders_number,
#          'delivered_orders_month':delivered_orders_month,
#          'delivered_orders_by_months':delivered_orders_by_months,
#     }
#     return render(request, 'admin/admin_panel.html', context)


@login_required(login_url='admin_login')
def admin_panel(request):
    today = date.today()
    
    delivered_orders = Order.objects.filter(status='Delivered')
    
    delivered_orders_by_months = delivered_orders.annotate(
        delivered_month=ExtractMonth('created_at'),
        delivered_day=ExtractDay('created_at')
    ).values('delivered_month', 'delivered_day').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_day', 'delivered_count')
    
    delivered_orders_month = []
    delivered_orders_number = []
    for d in delivered_orders_by_months:
        month_name = calendar.month_name[d['delivered_month']]
        day_number = d['delivered_day']
        delivered_orders_month.append(f"{month_name} {day_number}")
        delivered_orders_number.append(d['delivered_count'])

    order_by_months = Order.objects.annotate(
        month=ExtractMonth('created_at'),
        day=ExtractDay('created_at')
    ).values('month', 'day').annotate(count=Count('id')).values('month', 'day', 'count')
    
    monthNumber = []
    dayNumber = []
    totalOrders = []
    for o in order_by_months:
        month_name = calendar.month_name[o['month']]
        day_number = o['day']
        monthNumber.append(f"{month_name} {day_number}")
        dayNumber.append(day_number)
        totalOrders.append(o['count'])

    delivered_orders_by_years = delivered_orders.annotate(delivered_year=ExtractYear('created_at')).values('delivered_year').annotate(delivered_count=Count('id')).values('delivered_year', 'delivered_count')
    delivered_orders_year = []
    delivered_orders_year_number = []
    for d in delivered_orders_by_years:
        delivered_orders_year.append(d['delivered_year'])
        delivered_orders_year_number.append(d['delivered_count'])
    
    order_by_years = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')
    yearNumber = []
    totalOrdersYear = []
    for o in order_by_years:
        yearNumber.append(o['year'])
        totalOrdersYear.append(o['count'])
    
    context ={
        'delivered_orders': delivered_orders,
        'order_by_months': order_by_months,
        'monthNumber': monthNumber,
        'dayNumber': dayNumber,
        'totalOrders': totalOrders,
        'delivered_orders_number': delivered_orders_number,
        'delivered_orders_month': delivered_orders_month,
        'delivered_orders_by_months': delivered_orders_by_months,
        'today': today,
        'order_by_years': order_by_years,
        'yearNumber': yearNumber,
        'totalOrdersYear': totalOrdersYear,
        'delivered_orders_year': delivered_orders_year,
        'delivered_orders_year_number': delivered_orders_year_number,
        'delivered_orders_by_years': delivered_orders_by_years,
    }
    return render(request, 'admin/admin_panel.html', context)


def sales_report(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'admin/sales_report.html', context)


def sales_report_by_product(request, id):
    product = Product.objects.get(pk=id)
    orders = OrderProduct.objects.filter(product=product)
    s = product.product_variant.all()
    total_stock = 0
    for s in s:
      total_stock += s.stock
      
    delivered_orders = []
    delivered_quantity = 0
    for order in orders:
        if order.order.status == 'Delivered':
           delivered_orders.append(order)
           delivered_quantity += order.quantity
    
    number_delivered_orders = len(delivered_orders)

    
    context = {
        'product':product,
        'orders':orders,
        'delivered_quantity':delivered_quantity,
        'number_delivered_orders':number_delivered_orders,
        'total_stock':total_stock,
    }
    return render(request, 'admin/sales_report_by_product.html', context)


def sales_date(request):
    if request.method == 'GET':
        form = DateFilterForm(request.GET)
        # order_by_date = Orders.objects.annotate(month=ExtractDay('created_at')).values('day').annotate(count=Count('id')).values('day','count')
        # totalOrders = []
        # for o in order_by_date:
        #  totalOrders.append(list(o.values())[1])

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Query the sales data within the specified date range
            sales_data = Order.objects.filter(created_at__range=[start_date, end_date])

            return render(request, 'admin/sales-report-daily.html', {'sales_data': sales_data, 'form': form,})
    else:
        form = DateFilterForm()

    return render(request, 'admin/sales-report-daily.html', {'form': form})


# admin login page
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['Password']
        user = authenticate(email=email,password=password)

        if user is not None and user.is_superuser:
            login(request,user)
            return redirect("admin_panel")
        else:
            messages.error(request,"User name or password is incorect")
            return redirect('admin_login')
    return render(request,"admin/admin_login.html")


# admin logout 
def admin_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "logged out succesfully")
    return redirect('admin_login')


# admin user management
def user(request):
    if request.method=="POST":
        fm = Aforms(request.POST)
        if fm.is_valid():
            fm.save()
            fm = Aforms()
    else:
        fm = Aforms()
    
    stud=CustomUser.objects.all()
    return render(request,'admin/user.html',{'fm':fm,'stud':stud})


# admin side user search
def search(request):
    users = []
    if request.method == 'POST':
        query = request.POST['query']
        users = CustomUser.objects.filter(Q(email__icontains=query)|Q(id__contains=query))
    return render(request, "admin/search.html", {'users':users})


# block user 
def block_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
        
        # Check the referer to determine the redirect URL
        referer = request.META.get('HTTP_REFERER')

        if 'search' in referer:
            # Redirect to search page
            
            return redirect('user')
        else:
            # Redirect to user page
            return redirect('user')


# unblock user 
def unblock_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
        # Check the referer to determine the redirect URL
        referer = request.META.get('HTTP_REFERER', '')

        if 'search' in referer:
            # Redirect to search page
            return redirect('search')
        else:
            # Redirect to user page
            return redirect('user')

# admin products management   
def products(request):
    pro = Product.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/products.html', context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('products')
    else:
        product_form = ProductForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin/product_edit.html', context)


def del_product(request, id):
    if request.method == "POST":
        prod = Product.objects.get(pk=id)
        prod.delete()
        return redirect('products')

def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        image_form = ProductImageFormSet(request.POST, request.FILES, instance=Product())
        if product_form.is_valid() and image_form.is_valid():
            myproduct = product_form.save(commit=False)
            myproduct.save()
            image_form.instance = myproduct
            image_form.save()

            # for form in image_form:
            #     if form.cleaned_data and 'image' in form.cleaned_data:
            #         image_instance = form.cleaned_data['image']
            #         image_path = image_instance.path
            #         with Image.open(image_path) as img:
            #             width, height = img.size

            return redirect("products")
    else:
        product_form = ProductForm()
        image_form = ProductImageFormSet(instance=Product())
    context = {'product_form': product_form, 'image_form': image_form}
    return render(request, 'admin/add_product.html', context)


# admin product variant management

def product_variant(request):
    pro = ProductVariant.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/product_variant.html', context)

def del_product_variant(request, id):
    if request.method == "POST":
        prod = ProductVariant.objects.get(pk=id)
        prod.delete()
        return redirect('product_variant')

def add_product_variant(request):
    if request.method == "POST":
        product_form = VariantForm(request.POST,request.FILES)
        # image_form = ProductImageFormSet(request.POST, request.FILES, instance=product())
        if product_form.is_valid():
            # myproduct = product_form.save(commit=False)
            product_form.save()
            # image_form.instance = myproduct
            # image_form.save()
            # return redirect('products')
            return redirect("product_variant")
    else:
        product_form = VariantForm()
        # image_form = ProductImageFormSet(instance=product())
    context = {'product_form': product_form}
    return render(request, 'admin/add_product_variant.html', context)

def edit_product_variant(request, id):
    product = get_object_or_404(ProductVariant, pk=id)
    if request.method == "POST":
        product_form = VariantForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('product_variant')
    else:
        product_form = VariantForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin/product_variant_edit.html', context)


# admin category management

def category(request):
    pro = Category.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/category.html', context)

def del_category(request, id):
    if request.method == "POST":
        prod = Category.objects.get(pk=id)
        prod.delete()
        return redirect('category')

def edit_category(request, id):
    product = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        product_form = CategoryForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('category')
    else:
        product_form = CategoryForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin/category_edit.html', context)

def add_category(request):
    if request.method == "POST":
        product_form = CategoryForm(request.POST,request.FILES)
        # image_form = ProductImageFormSet(request.POST, request.FILES, instance=product())
        if product_form.is_valid():
            # myproduct = product_form.save(commit=False)
            product_form.save()
            # image_form.instance = myproduct
            # image_form.save()
            # return redirect('products')
            return redirect("category")
    else:
        product_form = CategoryForm()
        # image_form = ProductImageFormSet(instance=product())
    context = {'product_form': product_form}
    return render(request, 'admin/add_category.html', context)


# admin brand management

def brand(request):
    pro = Brand.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/brand.html', context)

def del_brand(request, id):
    if request.method == "POST":
        prod = Brand.objects.get(pk=id)
        prod.delete()
        return redirect('brand')

def edit_brand(request, id):
    product = get_object_or_404(Brand, pk=id)
    if request.method == "POST":
        product_form = BrandForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('brand')
    else:
        product_form = BrandForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin/brand_edit.html', context)

def add_brand(request):
    if request.method == "POST":
        product_form = BrandForm(request.POST,request.FILES)
        # image_form = ProductImageFormSet(request.POST, request.FILES, instance=product())
        if product_form.is_valid():
            # myproduct = product_form.save(commit=False)
            product_form.save()
            # image_form.instance = myproduct
            # image_form.save()
            # return redirect('products')
            return redirect("brand")
    else:
        product_form = BrandForm()
        # image_form = ProductImageFormSet(instance=product())
    context = {'product_form': product_form}
    return render(request, 'admin/add_brand.html', context)

def color(request):
    pro = Color.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/color.html', context)

def add_color(request):
    if request.method == "POST":
        product_form = ColorForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect("color")
    else:
        product_form = ColorForm()
    context = {'product_form': product_form}
    return render(request, 'admin/add_color.html', context)

def del_color(request, id):
    if request.method == "POST":
        prod = Color.objects.get(pk=id)
        prod.delete()
        return redirect('color')

def size(request):
    pro = Size.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/size.html', context)

def add_size(request):
    if request.method == "POST":
        product_form = SizeForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_form.save()
            
            return redirect("size")
    else:
        product_form = SizeForm()
    context = {'product_form': product_form}
    return render(request, 'admin/add_size.html', context)


def del_size(request, id):
    if request.method == "POST":
        prod = Size.objects.get(pk=id)
        prod.delete()
        return redirect('size')


def orders(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, 'admin/admin_myorder.html', {'orders':orders})


def ordersearch(request):
    users = []
    if request.method == 'POST':
        query = request.POST['query']
        # orders = CustomUser.objects.filter(Q(email__icontains=query)|Q(id__contains=query))
        orders = Order.objects.filter(Q(user__email__icontains=query) | Q(user__id__contains=query)).order_by("-created_at")

        # order = Order.objects.filter(order=orders)
    return render(request, "admin/order-search.html", {'orders':orders})


def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
            order = Order.objects.get(pk=id)
            order.status = status
            order.save()
            if status == 'Delivered':
                payment = order.payment
               
                payment.status = 'Success'
                payment.save()


        except Order.DoesNotExist:
            pass
    return redirect("orders")


#fetch each products from order
def order_products(request, id):
    orders = Order.objects.get(pk=id)
    myorder = OrderProduct.objects.filter(order=orders)
    add = orders.address
    context = {
        'orders': orders,
        'myorder':myorder,
        'add': add,
    }
    return render(request, 'admin/admin_orderproducts.html', context) 





# def order_tracker(request):
#     if request.method=="POST":
#         orderId = request.POST.get('orderId', '')
#         try:
#             order=Order.objects.filter(pk=orderId)

#             if len(order)>0:
#                 update = Order.objects.filter(pk=orderId)
#                 updates = []
#                 for order in update:
#                     # change order status to scheduled
#                     if order.status == 'processing':
#                         order.status = 'scheduled'
#                         order.save()
#                     updates.append({'status' : order.status})
#                     response = json.dumps(updates)
#                     return HttpResponse(response)
#             else:
#                 return HttpResponse('{}')
#         except Exception as e:
#             # add some logging here
#             return HttpResponse('{}')
#     return render(request,"admin/order_status.html")


def coupon_manage(request):
    coupon = Coupon.objects.all()
    context = {
        "coupon" : coupon,
    }
    return render(request,'admin/coupon.html', context)


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon_manage')
    else:
        form = CouponForm()

    context = {'form': form}
    return render(request, 'admin/add_coupon.html', context)


def del_coupon(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        coup.delete()
    return redirect('coupon_manage')


def edit_coupon(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        form = CouponForm(request.POST, instance=coup)
        if form.is_valid:
            form.save()
        return redirect('coupon_manage')
    else:
        coup = Coupon.objects.get(id=id)
        form = CouponForm(instance=coup)
        context = {
            "form" : form
        }
    return render(request, 'admin/edit_coupon.html', context)



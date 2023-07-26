from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from products . models import *
from . forms import *
from . import verify
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from order.models import *
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from order.models import *
from  cart.models import *
import json
from django.core.exceptions import ObjectDoesNotExist
import decimal



# Create your views here.


# signup page

def signup(request):

    email = request.session.get('email')
    if email:
        return redirect('home')
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if pass1 == pass2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request,"User already exists")
                return redirect('signup')
            else:
                user = CustomUser.objects.create_user(email=email, name=name, phone_number=phone, password=pass1)
                user.save()

                return redirect("signin")
        else:
            messages.info(request, 'Password do not match')
            return redirect('signup')

    return render(request,"signup.html")


# signin page
def signin(request):

    email = request.session.get('email')

    if email:
        return redirect('home')
   
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['Password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            request.session['email']=email
            messages.info(request,'Logged in succesfully')
            return redirect("home")
        else:
            messages.error(request,"User name or password is incorrect")
            return redirect('signin')
    return render(request,"signin.html")


def signout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "logged out succesfuly")
    return redirect('home')


def home(request):
    pro = Product.objects.all()
    price_filter_form = PriceFilterForm(request.GET or None)
    context={
        'pro': pro,
        'price_filter_form': price_filter_form
    }
    return render(request, "index.html", context)


def product_details(request, id):
    pro = Product.objects.get(pk=id)
    var = ProductVariant.objects.all()
    # size = Size.objects.all()
    # color = Color.objects.all()
    return render(request, 'product-detail.html', {'pro' : pro})


def search_brand(request):
    # product = []
    if request.method == 'POST':
        query = request.POST['query']
        product = Product.objects.filter(Q(id__contains=query)|Q(Brand__brand_name__icontains=query)|Q(product_name__icontains=query))
    return render(request, "search_brand.html", {'product':product})    


def men(request):
    product = Product.objects.filter(gender="Male")
    return render(request, "men.html", {'product':product})


def women(request):
    product = Product.objects.filter(gender="Female")
    return render(request, "women.html", {'product':product})


# user profile function
@login_required(login_url='signin')
def userprofile(request):
    address = Address.objects.filter(user=request.user)
    order = OrderProduct.objects.filter(user=request.user)
    user=request.user

    print(user)


    context = {
        'address': address,
        'order': order,
        'user': user,
    }
    return render(request, 'user-profile.html', context)


def Address_book(request):
    address = Address.objects.filter(user=request.user)

    context = {
        'address': address,
    }
    return render(request, 'address.html', context)


def myorders(request):
    order = OrderProduct.objects.filter(user=request.user).order_by("-created_at")
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    context = {
        'order': order,
        'orders': orders,
    }
    return render(request, 'myorders.html', context)


def myorder_products(request, id):
    orders = Order.objects.get(pk=id)
    
    myorder = OrderProduct.objects.filter(order=orders)
    add = orders.address

    context = {
        'orders': orders,
        'myorder':myorder,
        'add': add,
    }
    return render(request, 'myorders_products.html', context) 


def wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
        if wallet:
            print(wallet.balance)
    except:
        wallet = Wallet.objects.create(user=request.user, balance=0)
    return render(request,'wallet.html',{'wallet':wallet})

#order cancel function
def cancel_order(request,id):
    print(id)
    if request.method == "POST":
        cancellation_reason = request.POST.get('cancellation_reason')
        try:
        
            order = get_object_or_404(Order, pk=id, user=request.user)
            orders = OrderProduct.objects.filter(order=order)
            order.status = 'Cancelled'
            order.cancellation_reason = cancellation_reason
            order.save()
            if order.status == 'Cancelled':
                for product in orders:
                    product.variation.stock += product.quantity
                    product.variation.save()
                

            if order.payment.payment_method =='Razorpay':
                wallet, _ =Wallet.objects.get_or_create(user=request.user)
                refund_amount=decimal.Decimal(order.order_total)
                wallet.balance += refund_amount
                wallet.save()

        except Order.DoesNotExist:
            pass
    return redirect("myorders")


#order return function
def return_order(request,id):
    print(id)
    if request.method=="POST":
        return_reason=request.POST.get('return_reason')
        try:
            order = get_object_or_404(Order, pk=id, user= request.user)
            order.status='Return'
            order.return_reason = return_reason
            order.save()
            if order.payment.payment_method == 'Razorpay' or 'COD':
                wallet, _ = Wallet.objects.get_or_create(user=request.user)
                refund_amount = decimal.Decimal(order.order_total)
                print(refund_amount)
                wallet.balance += refund_amount
                wallet.save()

        except Order.DoesNotExist:
            pass
    return redirect('myorders')


@login_required(login_url='signin')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html',context)


def add_to_wishlist(request, id):
    myproduct = get_object_or_404(Product, pk=id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=myproduct)
    response_data = {'created': created}
    return JsonResponse(response_data)


def remove_from_wishlist(request, id):
    myproduct = get_object_or_404(Product, pk=id)
    Wishlist.objects.filter(user=request.user, product=myproduct).delete()
    messages.success(request, 'Product removed from wishlist.')
    return redirect('wishlist')


def apply_coupon(request):
    print('Coupon starts')
    if request.method == 'POST':
        data = {}
        body = json.loads(request.body)
        coupon_code = body.get('coupon')
        print(coupon_code)
        total_price = body.get('total_price')
        print(total_price)

        try:
            coupon = Coupon.objects.get(coupon_code__iexact=coupon_code, is_expired=False)
        except Coupon.DoesNotExist:
            data['message'] = 'Not a Valid Coupon'
            data['total'] = total_price
        else:
            if coupon.is_expired:
                data['message'] = 'Coupon Already Used'
                data['total'] = total_price
            else:
                minimum_amount = coupon.minimum_amount
                discount_price = coupon.discount_price
                print(discount_price)
                if total_price >= minimum_amount:
                    total_price -= discount_price
                    request.session['total'] = total_price
                    coupon.is_expired = True
                    coupon.save()
                    print(total_price)
                    data['message'] = f'{coupon.coupon_code} Applied'
                    data['total'] = total_price 
                    print(data)
                else:
                    data['message'] = 'Not a Valid Coupon'
                    data['total'] = total_price
                    print('else')
                    print(data)

        return JsonResponse(data)


def filter_price(request):
    print("entered")
    product = Product.objects.all()
    price_filter_form = PriceFilterForm(request.GET or None)
    if price_filter_form.is_valid():
        min_price = price_filter_form.cleaned_data['min_price']
        max_price = price_filter_form.cleaned_data['max_price']
        product = [product for product in product if any(product.price >= min_price and product.price <= max_price for variant in product.product_variant.all())]

    context ={
        'product':product,
    }
    return render(request,'filter.html',context)


def about(request):
    return render(request, 'about.html')


# def contact(request):
#     return render(request, 'contact.html')
    

#otp-login
def verify_code(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_no = request.session.get('phone')
            # user = authenticate(request,phone_number=phone_no)
            if verify.check(phone_no, code):
                print("checked")
                user = CustomUser.objects.get(email = request.session.get('username'))
                userobj = CustomUser.objects.filter(email = request.session.get('username'))
            
                if userobj is not None and user.is_active and user.is_superuser == False:
                    print(user.is_authenticated)
                    login(request, user)
                    return redirect(home)
                print(user)
                return redirect(home)
            else:
                print("error")
    else:
        form = VerifyForm()
    return render(request, 'otp_verify.html', {'form': form})


def otp_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        phone = '+91'+  str(request.POST['phone_number'])
        if check_phone_number(request.POST['phone_number']):
            verify.send(phone)
            user = username_password(request.POST['phone_number'])
            if user is not None:
                request.session['username'] = user.email
                print(user.email)
                user.is_verified = True
                user.is_active = True
                request.session['phone'] = phone
                return redirect('verify_code')
            else:
                messages.error(request, "Please register first")
                return render(request, 'otp_login.html')
    return render(request, 'otp_login.html')

def username_password(phone):
    user = CustomUser.objects.filter(phone_number=phone).first()
    return user

def check_phone_number(phone_number):
    try:
        phone_number = CustomUser.objects.filter(phone_number=phone_number).first()
        return True
    except CustomUser.DoesNotExist:
        return False


# 
def forgotPassword(request):
    global mobile_number_forgotPassword
    if request.method == 'POST':
        # setting this mobile number as global variable so i can access it in another view (to verify)
        mobile_number_forgotPassword = request.POST.get('phone_number')
        # checking the null case
        if mobile_number_forgotPassword is '':
            messages.warning(request, 'You must enter a mobile number')
            return redirect('forgotPassword')
   
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        user = CustomUser.objects.filter(phone_number=mobile_number_forgotPassword)
        if user:  #if user exists
            verify.send('+91' + str(mobile_number_forgotPassword))
            return redirect('forgotPassword_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
            return redirect('forgotPassword')
            
    return render(request, 'forgotPassword.html')


def forgotPassword_otp(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('code')
        # otp = request.POST.get('otp')
        if verify.check('+91'+ str(mobile_number), otp):
            user = CustomUser.objects.get(phone_number=mobile_number)
            if user:
                return redirect('resetPassword')
        else:
            messages.warning(request,'Invalid OTP')
            return redirect('enter_otp')
    else:
        form = VerifyForm()
        
    return render(request,'forgotPassword_otp.html', {'form':form})


def resetPassword(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        print(str(password1)+' '+str(password2)) #checking
        
        if password1 == password2:
            user = CustomUser.objects.get(phone_number=mobile_number)
            print(user)
            print('old password  : ' +str(user.password))
            
            user.set_password(password1)
            user.save()

            print('new password  : ' +str(user.password))
            messages.success(request, 'Password changed successfully')
            return redirect('signin')
        else:
            messages.warning(request, 'Passwords doesnot match, Please try again')
            return redirect('resetPassword')
    
    return render(request, 'resetPassword.html')


from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from user_account.models import CustomUser
from products.models import *
from user_account.models import *
import json
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse
from . forms import *
from user_account.views import *
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def add_to_cart(request):  
        id = request.GET['productid']
        print(id)
        user = request.user if request.user.is_authenticated else None
        cart,_= Cart.objects.get_or_create(user=user)
        print(user)
        product =Product.objects.get(pk=id)      
        price = request.GET['selectedprice']
        size =request.GET['selectedsize']
        # quantity =request.GET['quantity']
        print(price)
        print(size)
        
        # print(quantity)
       
        size_id = Size.objects.filter(name=size).values_list('pk', flat=True).first()
        print(size_id)
        product_variant = ProductVariant.objects.get(product_name_id=id,size_id=size_id)
        print(product_variant)
    
        if product_variant:
             CartItem.objects.create(user=user,cart=cart,product=product,product_variant=product_variant)

            # cart_item,item_created = CartItem.objects.get_or_create(user=user,cart=cart,product=product)
            # if cart_item:
            #     print("there is an item")
            #     cart_item.quantity = cart_item.quantity + int(quantity)
            #     cart_item.save()
            # else:
            #     print("new item created")
     
        # else:
        #     text = "Out of stock"
        #     return render(request,'product_details.html',{'text':text})
        # context ={
        #     'product' :product,
        #     'cart_item' : cart_item           
        # }
        # # return render(request,'cart.html',context)

        return JsonResponse({'status':400,"message":"added"})

def delete_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='signin')
def cart(request):
    # user = request.user if request.user.is_authenticated else None
    user = request.user
    try:
        if user: 
            cart,_ = Cart.objects.get_or_create(user=user)
            print(cart)
            cart_items = CartItem.objects.filter(user=user)
            if cart_items:
                if (request.session.get('total')):
                    sum = request.session.get('total')
                else:
                # prod = cart_items.get_subtotal()
                    sum = cart.get_total_price()
                total = cart.get_total_products()
                coupon = Coupon.objects.all()
                context = {
                    'cart_items': cart_items,
                    'cart': cart,
                    'sum': sum,
                    'total': total,
                    "coupon" : coupon,
                    # 'prod': prod,
                }
                return render(request, 'cart.html', context)
            else:
                message = "Your Cart is Empty"
                return render(request, 'cart.html', {'message': message})
        else:
            raise Exception("User not authenticated")  # Raise an exception if the user is not authenticated
    except Exception as e:
        # Handle the exception appropriately
        # For example, you can log the error or display a user-friendly message
        error_message = f"Error occurred: {str(e)}"
        print(error_message)
        return redirect('home')
    return render(request, 'cart.html')


def update_cart_item_quantity(request):
        print('entered')
        cart = Cart.objects.get(user=request.user)
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')

        # cart_item = Cartitem.objects.get(id=cart_item_id)
        try:
           print('try')
           cart_item = CartItem.objects.get(id=cart_item_id) 
           print(cart_item)
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
            print("increases")
            if cart_item.product_variant.stock > cart_item.quantity:
                cart_item.quantity += 1
                print(cart_item.quantity)
        elif action == 'decrease':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
        cart_item.save()
        if 'total' in request.session:
            del request.session['total']

        return JsonResponse({'status': 200, 'quantity': cart_item.quantity,'total':cart.get_total_price(),'total_items':cart.get_total_products()})
    

# def admin_cart(request):
#      cart = Cart.objects.all()
#      cartitems = Cart.objects.all()
#      return render(request,'admin_cart.html',{'cart':cart,'cartitems':cartitems})


class Checkout(View):
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(user=request.user)
            address = Address.objects.filter(user=request.user)

            if cart_items.exists():
                if (request.session.get('total')):
                    sum = request.session.get('total')
                else:
                # prod = cart_items.get_subtotal()
                    sum = cart.get_total_price()
                # sum = cart.get_total_price()
                total = cart.get_total_products()

                context = {
                    'cart_items': cart_items,
                    'address': address,
                    'sum': sum,
                    'total': total,
                }
                return render(request, 'checkout.html', context)
            else:
                return redirect('cart')  # Redirect to cart page if there are no cart items
        except Cart.DoesNotExist:
            return redirect('cart')  # Redirect to cart page if the user doesn't have a cart

    
class Add_address(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'add-address.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Checkout')


class Add_address_user(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'add-address.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Address_book')


# edit address checkout page
def edit_addresss(request, id):
    product = get_object_or_404(Address, pk=id)
    if request.method == "POST":
        product_form = AddressForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('Checkout')
    else:
        product_form = AddressForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'edit-address.html', context)


# user profile edit address
def edit_addresss_user(request, id):
    product = get_object_or_404(Address, pk=id)
    if request.method == "POST":
        product_form = AddressForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('Address_book')
    else:
        product_form = AddressForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'edit-address.html', context)


def del_address(request, id):
    prod = Address.objects.get(pk=id)
    prod.delete()
    return redirect('Checkout')


def del_address_user(request, id):
    prod = Address.objects.get(pk=id)
    prod.delete()
    return redirect('Address_book')


def payment(request, id):
    cart = Cart.objects.get(user=request.user)
    adds = Address.objects.get(pk=id)
    if (request.session.get('total')):
        sum = request.session.get('total')
    else:
        sum = cart.get_total_price()
    # sum = cart.get_total_price()
    total = cart.get_total_products()
    try:
        wallet = Wallet.objects.get(user=request.user)
    except:
        wallet = Wallet.objects.create(user=request.user)

    
    
    if wallet.balance >= sum:
        flag = 1
    else:
        flag = 0
    # import razorpay
    # client = razorpay.Client(auth=("rzp_test_9PWZXmd88RGOGY", "CMlBW52kdSRZWeoUu5Dlt3Qv"))
                
    # razorpay_order = client.order.create(
    # {"amount": int(self.total_price), "currency": "INR", "payment_capture": "1"}
    #                                 )
    context = {
            'sum': sum,
            'total': total,
            'adds': adds,
            'flag': flag,
            # 'razorpay_order': razorpay_order,
        }
    return render(request, 'payment.html', context)



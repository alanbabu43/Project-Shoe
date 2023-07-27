from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from .models import *
from user_account.models import *
from products.models import *
from cart.models import *
from .models import *
from django.http import JsonResponse
from .forms import *
from cart.views import *
import datetime
import json

from django.urls import reverse
import razorpay



class place_order(View):

        def dispatch(self, request, *args, **kwargs):
                # Declare and assign instance attributes
                
                self.flag = 0
                print("place")
                self.current_user = request.user
                print(self.current_user)

                self.cart = Cart.objects.get(user=self.current_user)
                self.cart_items = CartItem.objects.filter(user=self.current_user)
                self.cart_count = self.cart_items.count()
                
                if (request.session.get('total')):
                        self.total_price = request.session.get('total')
                else:
                        self.total_price = self.cart.get_total_price()
                print(self.total_price)

                # self.total_price = self.cart.get_total_price()
                print(self.cart_count)
                self.default_address_id = None
                # Call the default dispatch method
                return super().dispatch(request, *args, **kwargs)
                        
                
            
        def get(self,request):
            
            
          # if cart count is less than or equal to zero redirect back to homepage
            if self.cart_count <= 0:
                    return redirect('home')
            else:
                print("else")
                try:
                        current_order = Order.objects.get(user=self.current_user)
                        print(current_order,"current")
                        if current_order:
                                data = self.current_order
                        else:
                                raise Exception("order not formed")
                except Exception as e:
                        print("exception")
                        data = Order()
                        print(data)

                        
                        data.user = self.current_user
                        selected_option = request.GET.get('selectedOption')
                        payment_method_mapping = {
                                        'cod': 'COD',
                                        'razorpay': 'Razorpay',
                                        # Add more mappings as needed
                                }
                        print(selected_option)
                        payment_method_selected = payment_method_mapping.get(selected_option)
                        # status =''
                        # if payment_method_selected == 'COD':
                        #         status = 'Pending'
                        # else:
                        #         status = 'Success'

                        print(payment_method_selected)
                        if selected_option == 'cod':
                                print("first one")
                                payment_method = Payment.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status="Pending")
                                
                                data.payment = payment_method
                                
                                self.default_address_id = request.GET.get('defaultAddressId')
                                print(self.default_address_id)
                                data.address =  Address.objects.get(id=self.default_address_id)
                                print(data.address)
                                data.order_total = self.total_price
                                print(data.user,data.payment,data.address,data.order_total)
                                data.save()
                                print(data)
                                # generate order number
                                yr = int(datetime.date.today().strftime('%Y'))
                                dt = int(datetime.date.today().strftime('%d'))
                                mt = int(datetime.date.today().strftime('%m'))
                                d = datetime.date(yr,mt,dt)
                                current_date = d.strftime("%Y%m%d")
                                order_number= current_date + str(data.id)
                                data.order_number = order_number
                                print(data.order_number,current_date)
                                data.save()
                                for item in self.cart_items:
                                        # discount = item.product_variant.price - self.total_price
                                        order = OrderProduct.objects.create(product=item.product,
                                                variation=item.product_variant,
                                                payment=payment_method,
                                                order=data,
                                                quantity=item.quantity,
                                                product_price=item.product_variant.price,
                                                user=self.current_user,
                                                ordered=True)
                                        print(order)
                                        print(item.product.stock)
                                        product = item.product_variant
                                        product.stock -= item.quantity
                                        print(item.product.stock)
                                        product.save()
                                        if 'total' in request.session:
                                                del request.session['total']
                                        item.delete()
                                        flag = 1
                                # redirect_url = reverse('payment') + f'?total={self.total_price}&id={order_id}'
                                redirect_url = reverse('complete_payment') + f'?amount={self.total_price}&order_number={order_number}&payment_id={payment_method.id}&address_id={self.default_address_id}'
                                return JsonResponse({'message': 'Order placed successfully.','flag':flag,'id':order_number,'amount':self.total_price,'redirect':redirect_url})
                        elif selected_option == 'razorpay':
                                    print("elif")
                                    import razorpay
                                    client = razorpay.Client(auth=("rzp_test_9PWZXmd88RGOGY", "CMlBW52kdSRZWeoUu5Dlt3Qv"))
                
                                    razorpay_order = client.order.create(
                                    {"amount": int(self.total_price), "currency": "INR", "payment_capture": "1"}
                                    )
                                    print(razorpay_order)
                                    
                                    order_id = razorpay_order['id']
                                    
                                    print(order_id)
                                        

                                    payment_method = Payment.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status="Success")
                                        
                                    data.payment = payment_method
                                        
                                    self.default_address_id = request.GET.get('defaultAddressId')
                                    data.address =  Address.objects.get(id=self.default_address_id)
                                    print(data.address)
                                    data.order_total = self.total_price
                                    print(data.user,data.payment,data.address,data.order_total)
                                    data.save()
                                    print(data)
                                    # generate order number
                                    yr = int(datetime.date.today().strftime('%Y'))
                                    dt = int(datetime.date.today().strftime('%d'))
                                    mt = int(datetime.date.today().strftime('%m'))
                                    d = datetime.date(yr,mt,dt)
                                    current_date = d.strftime("%Y%m%d")
                                    order_number= current_date + str(data.id)
                                    data.order_number = order_number
                                    print(data.order_number,current_date)
                                    data.save()
                                    for item in self.cart_items:
                                        order = OrderProduct.objects.create(product=item.product,
                                                variation=item.product_variant,
                                                payment=payment_method,
                                                order=data,
                                                quantity=item.quantity,
                                                product_price=item.product_variant.price,
                                                user=self.current_user,
                                                ordered=True)
                                        print(order)
                                        item.delete()
                                        variant = item.product_variant
                                        variant.stock -= item.quantity
                                        print(variant.stock)
                                        variant.save()
                             
                                    payment_id = payment_method.id
                                    redirect_url = reverse('razorpay') + f'?total={self.total_price}&id={order_id}&order_number={order_number}&payment_id={payment_id}&address_id={self.default_address_id}'
                                    return JsonResponse({'message': 'razorpay entered.','redirect':redirect_url})

def razorpay(request):
        # total = request.GET.get('total')
        if (request.session.get('total')):
                total = request.session.get('total')
                raz = total
        else:
                total = request.GET.get('total')
                raz = total
        try:
                total = float(total) * 100
        except (TypeError, ValueError):
                total = 0
        # total = total * 100
        if 'total' in request.session:
                del request.session['total']
        address_id=request.GET.get('address_id')
        # address = Address.objects.get(id=address_id)
        print(total)
        id = request.GET.get('id')
        order_number = request.GET.get('order_number')
        print(order_number)
        print(id)
        context = {
                'total': total,
                'id': id,
                'order_number': order_number,
                'raz': raz,
                'address_id': address_id,
        }
        return render(request, "razorpay.html", context)


# order placing and payment using wallet
def wallet_pay(request):
          
        current_user = request.user
        wallet = Wallet.objects.get(user=current_user)
        cart = Cart.objects.get(user=current_user)
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        # total_price = cart.get_total_price()
        if (request.session.get('total')):
                total_price = request.session.get('total')
        else:
                total_price = cart.get_total_price()
        
                
            
          # if cart count is less than or equal to zero redirect back to homepage
        if cart_count <= 0:
                return redirect('homepage')
        else:        
               
                data = Order()

                data.user = current_user

                payment_method = Payment.objects.create(user=current_user,payment_method='Wallet',amount_paid=total_price,status="Success")
                
                data.payment = payment_method
                
                default_address_id = request.GET.get('defaultAddressId')
                print(default_address_id)
                data.address =  Address.objects.get(id=default_address_id)
                print(data.address)
                data.order_total = total_price
                print(data.user,data.payment,data.address,data.order_total)
                data.save()
                print(data)
                # generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d")
                order_number= current_date + str(data.id)
                data.order_number = order_number
                print(data.order_number,current_date)
                data.save()
                for item in cart_items:
                        order = OrderProduct.objects.create(user=request.user,
                                product=item.product,
                                variation=item.product_variant,
                                payment=payment_method,
                                order=data,
                                quantity=item.quantity,
                                product_price=item.product_variant.price,
                                ordered=True)
                        print(order)
                        print(item.product_variant.stock)
                        p = item.product_variant
                        p.stock -= item.quantity
                        print(item.product_variant.stock)
                        p.save()
                        if 'total' in request.session:
                                del request.session['total']
                        item.delete()
                        
                cart.coupon = None
                cart.save()
                wallet.balance = float(wallet.balance) - float(total_price)
                wallet.save()
                redirect_url = reverse('complete_payment') + f'?amount={total_price}&order_number={order_number}&payment_id={payment_method.id}&address_id={default_address_id}'
                return JsonResponse({'message': 'Order placed successfully.','id':order_number,'amount':total_price,'redirect':redirect_url})


def complete_payment(request):
        id = request.GET.get('id')
        payment_id = request.GET.get('payment_id')
        print(payment_id)
        payment_method = Payment.objects.filter(user=request.user)
        amount = request.GET.get('amount')
        if payment_method == "razorpay":
                amount = float(amount)/100
        order_number = request.GET.get('order_number')
        address_id=request.GET.get('address_id')
        print(address_id)
        address = Address.objects.get(id=address_id)
        print(address)
        print(order_number)
        print(amount)
        context = {
                'id': id,
                'payment_id': payment_id,
                'amount': amount,
                'order_number': order_number,
                'address': address,
                }
        return render(request, "order-complete.html", context)


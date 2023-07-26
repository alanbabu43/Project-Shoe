from django.urls import path
from . import views
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cart', views.cart,name="cart"),
    path('add_to_cart', views.add_to_cart,name="add_to_cart"),
    path('delete_cart_item/<int:id>/', views.delete_cart_item,name="delete_cart_item"),
    path('update_cart_item_quantity', views.update_cart_item_quantity,name="update_cart_item_quantity"),

    
    path('checkout', Checkout.as_view(),name="Checkout"),
    path('add_address', Add_address.as_view(),name="Add_address"),
    path('Add_address_user', Add_address_user.as_view(),name="Add_address_user"),

    path('edit_addresss/<int:id>/', views.edit_addresss,name="edit_addresss"),
    path('edit_addresss_user/<int:id>/', views.edit_addresss_user,name="edit_addresss_user"),

    path('del_address/<int:id>/', views.del_address,name="del_address"),
    path('del_address_user/<int:id>/', views.del_address_user,name="del_address_user"),

    path('payment/<int:id>/', views.payment,name="payment"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
  path('', views.home,name="home"),
  path('search_brand', views.search_brand,name="search_brand"),

  path('forgotPassword', views.forgotPassword,name="forgotPassword"),
  path('forgotPassword_otp', views.forgotPassword_otp,name="forgotPassword_otp"),
  path('resetPassword', views.resetPassword,name="resetPassword"),

  path('signup', views.signup,name="signup"),
  path('signin', views.signin,name="signin"),
  path('signout', views.signout,name="signout"),
  path('otp_login', views.otp_login,name="otp_login"),
  path('verify_code', views.verify_code,name="verify_code"),
  path('signout', views.signout,name="signout"),

  path('product_details/<int:id>/', views.product_details,name="product_details"),
  path('men', views.men,name="men"),
  path('women', views.women,name="women"),

  path('userprofile', views.userprofile,name="userprofile"),
  path('Address_book', views.Address_book,name="Address_book"),
  path('myorders', views.myorders,name="myorders"),
  path('myorder_products/<int:id>/', views.myorder_products,name="myorder_products"),
  
  path('wishlist', views.wishlist,name="wishlist"),
  path('wallet', views.wallet,name="wallet"),
  path('add_to_wishlist/<int:id>/', views.add_to_wishlist,name="add_to_wishlist"),
  path('remove_from_wishlist/<int:id>/', views.remove_from_wishlist,name="remove_from_wishlist"),

  path('apply_coupon', views.apply_coupon,name="apply_coupon"),

  path('about', views.about,name="about"),
  path('filter_price', views.filter_price,name="filter_price"),
  # path('contact', views.contact,name="contact"),

  path('cancel_order/<int:id>/', views.cancel_order,name="cancel_order"),
  path('return_order/<int:id>/', views.return_order,name="return_order"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

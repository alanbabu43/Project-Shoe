from django.urls import path
from . import views
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('place_order', place_order.as_view(),name="place_order"),
    path('wallet_pay', views.wallet_pay,name="wallet_pay"),
    path('razorpay',views.razorpay,name="razorpay"),
    path('complete_payment',views.complete_payment,name="complete_payment"),

  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

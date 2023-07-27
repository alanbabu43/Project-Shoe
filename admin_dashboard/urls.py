from django.urls import path
from . import views

urlpatterns = [
  path('admin_panel', views.admin_panel,name="admin_panel"),
  path('sales_report_by_product/<int:id>/', views.sales_report_by_product,name="sales_report_by_product"),
  path('sales_report', views.sales_report,name="sales_report"),
  path('sales_date', views.sales_date,name="sales_date"),
  path('admin_login', views.admin_login,name="admin_login"),
  path('admin_logout', views.admin_logout,name="admin_logout"),

  path('user', views.user,name="user"),
  path('search', views.search,name="search"),
  path('block_user/<int:id>/', views.block_user,name="block_user"),
  path('unblock_user/<int:id>/', views.unblock_user,name="unblock_user"),

  path('products', views.products,name="products"),
  path('del_product/<int:id>/', views.del_product,name="del_product"),
  path('edit_product/<int:id>/', views.edit_product,name="edit_product"),
  path('add_product', views.add_product,name="add_product"),

  path('product_variant', views.product_variant,name="product_variant"),
  path('del_product_variant/<int:id>/', views.del_product_variant,name="del_product_variant"),
  path('edit_product_variant/<int:id>/', views.edit_product_variant,name="edit_product_variant"),
  path('add_product_variant', views.add_product_variant,name="add_product_variant"),

  path('category', views.category,name="category"),
  path('edit_category/<int:id>/', views.edit_category,name="edit_category"),
  path('del_category/<int:id>/', views.del_category,name="del_category"),
  path('add_category', views.add_category,name="add_category"),

  path('brand', views.brand,name="brand"),
  path('del_brand/<int:id>/', views.del_brand,name="del_brand"),
  path('edit_brand/<int:id>/', views.edit_brand,name="edit_brand"),
  path('add_brand', views.add_brand,name="add_brand"),

  path('color', views.color,name="color"),
  path('add_color', views.add_color,name="add_color"),
  path('del_color/<int:id>/', views.del_color,name="del_color"),

  path('size', views.size,name="size"),
  path('add_size', views.add_size,name="add_size"),
  path('del_size/<int:id>/', views.del_size,name="del_size"),

  path('orders', views.orders,name="orders"),
  path('edit_order/<int:id>/', views.edit_order,name="edit_order"), 
  path('ordersearch', views.ordersearch,name="ordersearch"), 

  path('coupon_manage', views.coupon_manage,name="coupon_manage"),   
  path('add_coupon', views.add_coupon,name="add_coupon"),   
  path('del_coupon/<int:id>/', views.del_coupon,name="del_coupon"),   
  path('edit_coupon/<int:id>/', views.edit_coupon,name="edit_coupon"), 

  path('order_products/<int:id>/', views.order_products,name="order_products"),   


]

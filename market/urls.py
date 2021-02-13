from django.urls import path

from . import views

urlpatterns = [
    # products urls
    path('product/insert/', views.product_insert, name='product_insert'),
    path('product/list/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('product/<int:product_id>/edit_inventory/', views.product_edit, name='product_edit'),

    path('customer/register/', views.customer_register, name='customer_register'),
    path('customer/list/', views.customer_list, name='customer_list'),
    path('customer/<int:customer_id>/', views.customer_details, name='customer_detail'),
    path('customer/<int:customer_id>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/logout/', views.customer_logout, name='customer_logout'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('shopping/cart/', views.shopping_cart, name='shopping_cart'),
    path('shopping/cart/add_items/', views.add_items, name='add_items'),
    path('shopping/cart/remove_items/', views.remove_items, name='remove_items'),
    path('shopping/submit/', views.submit_order, name='submit_order'),

]

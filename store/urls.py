from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('/detail/<int:pk>/', views.products_detail, name='products_detail'),
    path('search/', views.search_result, name='search_result'),
    path('store/<int:pk>/leave-comment/', views.leave_comment, name='leave_comment'),
    path('cart/', views.cart, name='cart'),
    path('edit_cart/<int:pk>/', views.edit_cart_item, name='edit_cart_item'),
    path('delete_cart_item/<int:pk>/', views.delete_cart_item, name='delete_cart_item'),
    path('orders/', views.orders, name='orders'),
    path('cart/create_order/', views.create_order, name='create_order'),
    path('rate_product/<int:pk>/', views.rate_product, name='rate_product'),
]
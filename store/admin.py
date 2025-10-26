from django.contrib import admin
from .models import Products, Slide, Comment, CartItem, Order, OrderProdect, Review
admin.site.register(Products)
admin.site.register(Slide)
admin.site.register(Comment)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderProdect)
admin.site.register(Review)
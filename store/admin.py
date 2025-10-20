from django.contrib import admin
from .models import Products, Slide, Comment, CartItem
admin.site.register(Products)
admin.site.register(Slide)
admin.site.register(Comment)
admin.site.register(CartItem)
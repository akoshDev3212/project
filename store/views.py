from django.shortcuts import render,reverse, redirect
from .models import Products, Slide, CartItem, Order, OrderProdect, Review
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,Http404
from .models import Comment, CartItem
from . import forms
def store(request):
    product_id = request.GET.get('product')
    slides = Slide.objects.all()
    products = Products.objects.all()
    if product_id:
        product = Products.objects.get(pk=product_id)
        cart_item =CartItem.objects.filter(product=product)
        if not cart_item:
            cart_item = CartItem.objects.create(customer=request.user, product=product, quantity=1)
            cart_item.save()
            return redirect('store:store')
        for item in cart_item:
            item.quantity += 1
            item.save()
    return render(request, 'store.html', {'slides': slides, 'products': products})



def products_detail(requist,pk):
    product = Products.objects.get(pk=pk)
    return render(requist, 'products_detail.html', {'product': product})

def search_result(request):
    query = request.GET.get('search')
    search_obj = Products.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
    return render(request,'search.html', {'search_obj':search_obj,
    'query':query})


def leave_comment(request, pk):
    try:
        news = Products.objects.get(pk=pk)
    except:
        raise Http404("Sahifa error")
    
    if request.user.is_authenticated:
        news.comments.create(comment_text=request.POST.get('comment_text'))
    
    else:
        news.comments.create(comment_text=request.POST.get('comment_text'))
        comment = Comment.objects.all()
    return HttpResponseRedirect(reverse('store:products_detail', args=(news.id,)))


def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    print([item.total_price() for item in cart_items])
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'total_quantity': total_quantity})


def edit_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    action = request.GET.get('action')

    if action == 'take' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('store:cart')
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('store:cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('store:cart')



def delete_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.delete()
    return redirect('store:cart')


def create_order(request):
    cart_items = CartItem.objects.all()
    total_price = sum([item.total_price() for item in cart_items])
    amount = sum([item.quantity for item in cart_items])
    form = forms.OrderForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_price=total_price,
            User=request.user
        )
        for cart_item in cart_items:
            OrderProdect.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price(),
            )

        cart_items.delete()
        return redirect('store:store')
    form = forms.OrderForm()
    return render(request, 'order_creation_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'amount': amount,
        'form': form
    })


def orders(request):
    orders_list = Order.objects.filter(User=request.user)
    return render(request, 'orders.html', {'orders': orders_list})


def rate_product(request, pk):
    product = Products.objects.get(pk=pk)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        form = forms.RateForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('store:rate_product', pk=pk)
    form = forms.RateForm()
    return render(request, 'rate.html', {'form': form, 'product': product, 'reviews': reviews})
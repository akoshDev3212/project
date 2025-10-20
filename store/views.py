from django.shortcuts import render,reverse, redirect
from .models import Products, Slide, CartItem
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,Http404
from .models import Comment
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
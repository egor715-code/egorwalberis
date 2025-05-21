from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Cart, CartItem


def index(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj  
    }
    return render(request, "app/index.html", context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    categories = []
    categories.append(product.category)
    cur_category = product.category
    while cur_category.parent:
        categories.append(cur_category.parent)
        cur_category = cur_category.parent
    categories.reverse()
    context = {"product": product, "categories": categories}
    return render(request, "app/product_details.html", context)

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'app/cart.html', {'cart': cart})


def cart_add(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('product_detail', product_slug=product_slug)


def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_detail')
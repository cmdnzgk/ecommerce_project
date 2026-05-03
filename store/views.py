from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem
from django.contrib.auth.decorators import login_required

def product_list(request):
    category_id = request.GET.get("category")

    if category_id:
        products = Product.objects.filter(category_id = category_id)
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()

    return render(request, "product_list.html", {
        "products": products,
        "categories": categories,})

def product_detail(request, id):
    product = get_object_or_404(Product, id = id)

    return render(request, "product_detail.html", {"product": product})

login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id = product_id)

    cart, created = Cart.objects.get_or_create(user = request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart = cart,
        product = product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("product_list")
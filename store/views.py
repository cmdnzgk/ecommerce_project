from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib import messages


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

    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("product_list")

login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_items = CartItem.objects.filter(cart = cart)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })

login_required
def increase_quantity(request, item_id):
    item = CartItem.objects.get(id = item_id)
    item.quantity += 1
    item.save()

    return redirect("cart")

login_required
def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id = item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    
    return redirect("cart")

login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id = item_id)
    item.delete()

    return redirect("cart")

def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)

        return redirect("product_list")
    
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Hoşgeldiniz, {user}.")

            return redirect("product_list")

        else:
            messages.error(request, "Kullanıcı adı veya Şifre hatalı.")
    
    return render(request, "login.html")
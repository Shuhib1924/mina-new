from math import e
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import Product, Variation, Category, CartItem, Order
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
import json
from .forms import OrderForm

from escpos.printer import Network


def home(request):
    products = Product.objects.all().order_by("-created_date")[:4]
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, "p1/index.html", context)


def all_categories(request):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}


def category(request, cid):
    category = Category.objects.get(id=cid)
    products = Product.objects.filter(category=category)
    product_count = products.count()
    context = {
        "category": category,
        "products": products,
        "product_count": product_count,
    }
    return render(request, "p1/category.html", context)


def detail(request, pid):
    if request.session.session_key:
        print(
            Session.objects.get(pk=request.session.session_key).get_decoded(),
            request.session.session_key,
        )
    product = Product.objects.get(id=pid)
    context = {
        "product": product,
    }
    # return HttpResponse(f"{product.name}")
    return render(request, "p1/detail.html", context)


def add_cart(request):
    # *get or create session
    cart_session = request.session.get("cart")
    if not cart_session:
        cart_session = request.session.create()
        cart_session = request.session["cart"] = []

    print("cart_session", cart_session)
    # %2. selected product from request
    # cart_list = []
    if request.method == "POST":
        # $ check post request
        # print("post", request.POST, '\n')
        # * get product
        get_product_id = request.POST.get("product")
        selected_product = get_object_or_404(Product, id=get_product_id)
        print("selected_product", selected_product, "\n")
        # cart_session.append(selected_product)
        # request.session['cart']= cart

        get_variation_list = request.POST.getlist("variations[]")
        selected_variations = []
        for vid in get_variation_list:
            variation = get_object_or_404(Variation, id=vid)
            selected_variations.append(variation)
            print("variation", variation)
        print("selected_variations", selected_variations)
        # print("get_variation_list", get_variation_list)
        # selected_product = Product.objects.filter(id=get_product)
        # product = get_object_or_404(Product, id=get_product)
        # # cart_list.append(selected_product)
        # # print("cart_list", cart_list)
        # # print("get_product", get_product)
        # get_variation_list = request.POST.getlist('variations[]')
        # print("get_variation_list", get_variation_list)
        # @ create CartItem Object without variations
        cart_item = CartItem.objects.create(product=selected_product)
        # $ set the variations
        variations = Variation.objects.filter(id__in=get_variation_list)

        cart_item.variations.set(variations)
        # variations.update(selected=True)

        #  add into cart and save it into session
        cart_session.append({"cart_item": cart_item.id})
        request.session["cart"] = cart_session
        print(">>", request.session)
        # request.session['cart'] == cart_session
        # print(request.POST.getlist('variations[]'))
        # variations = request.POST.getlist('variations[]')
        # for i in variations:
        #     variation = Variation.objects.filter(name=i)
        #     print('variation', variation)

    #     # print(request.POST)
    # print([i for i in request.POST])
    # session_product = request.POST.get('product')
    # session_variation_list = request.POST.getlist('variations[]')
    # # % 3. save data to session
    # # request.session['selected_variations'] = session_variation_list
    # # request.session['product'] = session_product
    # # request.session.modified = True
    # product = Product.objects.get(name=session_product)
    # # print("product", product)
    # variations = Variation.objects.filter(name__in=session_variation_list)
    # # print("variations", variations)

    # return redirect('cart')
    return JsonResponse({"message": "success"})


def cart(request):
    data = request.session.get("cart", [])
    print("data", data)
    items = []
    if data:
        for el in data:
            obj = get_object_or_404(CartItem, id=el["cart_item"])
            print("obj", obj)
            items.append(obj)
    print("ITEMS", items)
    cart_sum = 0
    for ci in items:
        cart_sum = cart_sum + ci.pro_var_sum()
    # print("cart_sum", cart_sum)
    netto = cart_sum * 81 / 100
    tax = cart_sum * 19 / 100

    # if request.session.session_key:
    #         print(Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key)
    context = {
        "cart_sum": cart_sum,
        "netto": netto,
        "tax": tax,
        "items": items,
    }
    return render(request, "p1/cart.html", context)


def delete_item(request, id):
    item = get_object_or_404(CartItem, id=id)
    cart = request.session.get("cart", [])
    print("cart", cart, "\n")
    # delete from session
    for i in cart:
        if i["cart_item"] == id:
            cart.remove(i)
    print(cart)
    # save it into session
    request.session["cart"] = cart
    # delete from db
    item.delete()
    # return HttpResponse(f'CartItem ID: {item.id}<hr>Product: {item.product.name} <hr> items count: {len(cart)}<hr> key: {sk} <hr> all objects: {objects}<hr>')
    return redirect("cart")


def checkout(request):
    form = OrderForm()
    data = request.session.get("cart", [])
    print("data", data)
    items = []
    if data:
        for el in data:
            obj = get_object_or_404(CartItem, id=el["cart_item"])
            print("obj", obj)
            items.append(obj)
    print("ITEMS", items)
    cart_sum = 0
    for ci in items:
        cart_sum = cart_sum + ci.pro_var_sum()
    print("cart_sum", cart_sum)
    if request.session.session_key:
        print(
            Session.objects.get(pk=request.session.session_key).get_decoded(),
            request.session.session_key,
        )
    return render(request, "p1/checkout.html", {"form": form})


def printing(request):
    if request.session.session_key:
        print(
            Session.objects.get(pk=request.session.session_key).get_decoded(),
            request.session.session_key,
        )
    data = request.session.get("cart", [])
    print("data", data)
    items = []
    if data:
        for el in data:
            obj = get_object_or_404(CartItem, id=el["cart_item"])
            print("obj", obj)
            items.append(obj)
    print("ITEMS", items)
    cart_sum = 0
    for ci in items:
        cart_sum = cart_sum + ci.pro_var_sum()
    # print("cart_sum", cart_sum)
    netto = cart_sum * 81 / 100
    tax = cart_sum * 19 / 100

    if request.method == "POST":
        print(request.POST)
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        pickup_time = request.POST.get("pickup_time")
        order = Order.objects.create(name=name, phone=phone, pickup_time=pickup_time)
        # order.total = request.session
        # Set the IP address of the printer
        printer_ip = "192.168.178.177"
        # Initialize the network connection to the printer
        epson = Network(printer_ip)

        # Send data to the printer
        epson.text(f"{order.pickup_time}\n")
        epson.text(f"{order.id}\n")
        for el in data:
            obj = get_object_or_404(CartItem, id=el["cart_item"])
            print("obj", obj)
            epson.text(f"{obj.product}\n")
            for vl in obj.variations.all():
                epson.text(f"{vl}\n")

        epson.cut()

        # if order.daily_id.last() == None:
        #     order.daily_id =1
        # else:
        #     order.daily_id = order.daily_id + 1
        # order.save()
        context = {"order": order}

        # form = OrderForm(request.POST)
        # if form.is_valid():

        #     form.save(commit=False)

        #     form.daily_id +=1
        #     form.save()

        #     print('DID', form.daily_id)
        #     return HttpResponse('works')
        # else:
        #     return HttpResponse('error')
        # pickup_time = request.POST.get('pickup_time')
        # name = request.POST.get('name')
        # tel = request.POST.get('phone')

        # ! ganz am ende!!!!
        # request.session.flush()
    if request.method == "GET":
        return redirect("failed")
    return render(request, "p1/payment_success.html", context)


def payment_success(request):
    return HttpResponse("success")


def failed(request):
    return render(request, "p1/failed.html")

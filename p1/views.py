# from math import e
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import (
    Product,
    Variation,
    Category,
    Query,
    Order,
    Notification,
    Screen,
    Random,
)
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session

from django.core.exceptions import ObjectDoesNotExist
import json
from .forms import OrderForm
import random
from escpos.printer import Network

import ast


def notification(request):
    notifications = Notification.objects.filter(status=True)
    return {"notifications": notifications}


def home(request):
    screens = Screen.objects.order_by("rank")
    products = Product.objects.all().order_by("-created_date")[:6]
    context = {
        "products": products,
        "screens": screens,
    }

    return render(request, "p1/index.html", context)


def category(request, cslug):
    category = Category.objects.get(slug=cslug)
    products = Product.objects.filter(category=category)
    product_count = products.count()
    context = {
        "category": category,
        "products": products,
        "product_count": product_count,
    }
    return render(request, "p1/category.html", context)


def all_categories(request):
    all_categories = Category.objects.all().order_by("rank")
    return {"all_categories": all_categories}


def detail(request, pslug):
    product = Product.objects.get(slug=pslug)
    # print("product", product)
    queries = Query.objects.filter(product_query__name=product.name)
    # print("queries", queries)
    variations = Variation.objects.filter(
        query_variation__name__in=[i.name for i in queries]
    ).distinct()
    # print("variations", variations)

    context = {
        "product": product,
        "queries": queries,
        "variations": variations,
    }
    # return HttpResponse(
    #     f"{product.name}<hr> {list(queries.values())} <hr> {list(variations.values())}"
    # )
    return render(request, "p1/detail.html", context)


def cart(request):
    # #check cart
    cart_session = request.session.get("cart")
    if not cart_session:
        cart_session = request.session.create()
        cart_session = request.session["cart"] = []

    if request.method == "POST":
        # print(request.POST)
        users = ast.literal_eval(request.POST.get("users"))
        # ! this allow the user list to start the forloop
        if users == []:
            users = ["StrToAvoidError"]
        # @ divide users and add for each of them in session
        for i in users:
            if i == "StrToAvoidError":
                user = {"user": ""}
            else:
                user = {"user": i}
            # print("POST -user", user)
            try:
                product = {"product": request.POST.get("product")}
            except:
                product = {"product": ""}
            # print("POST - product", product)
            try:
                queries = {"queries": request.POST.getlist("queries")}
            except:
                queries = {"queries": []}
            # print("POST - queries", queries)
            try:
                variations = {"variations": request.POST.getlist("variations")}
            except:
                variations = {"variations": []}
            # print("POST - variations", variations)

            cart_session.append(
                {
                    "item": [
                        user,
                        product,
                        queries,
                        variations,
                    ]
                }
            )
        sorted_cart_session = sorted(
            cart_session, key=lambda item: item["item"][0].get("user", "")
        )
        # print("sorted_cart_session", sorted_cart_session)
        request.session["cart"] = sorted_cart_session
        request.session.modified = True

    # $ get modeldata from request.session
    cart_items = []
    # print(json.dumps(sorted_cart_session, indent=4))
    for item in request.session["cart"]:
        try:
            user = {"user": item["item"][0]["user"]}
        except:
            user = {"user": ""}
        # print("Q - user", user)
        try:
            product = {
                "product": get_object_or_404(Product, id=item["item"][1]["product"])
            }
        except:
            product = {"product": ""}
        # print("Q - product", product)
        try:
            queries = {
                "queries": get_list_or_404(
                    Query,
                    id__in=item["item"][2]["queries"],
                )
            }
        except:
            queries = {"queries": ""}
        # print("Q - queries", queries)
        try:
            variations = {
                "variations": get_list_or_404(
                    Variation, id__in=item["item"][3]["variations"]
                )
            }
        except:
            variations = {"variations": ""}
        # print("Q - variations", variations)
        try:
            item_price = product["product"].price + sum(
                [vp.price for vp in variations["variations"]]
            )
        except:
            item_price = product["product"].price
        # print("item_price", item_price)
        if not any("item_price" in el for el in item["item"]):
            item["item"].append({"item_price": float(item_price)})
        # item["item"].append({"item_price": float(item_price)})
        # print(item)
        cart_items.append(
            [user, product, queries, variations, {"item_price": item_price}]
        )
    request.session.modified = True
    print("cart_items", cart_items)
    context = {"cart_items": cart_items}
    return render(request, "p1/cart.html", context)


def cart_count(request):
    item_list = []
    if request.session.session_key:
        cart_count = len(request.session["cart"])
        for i in request.session["cart"]:
            item_list.append(i)
    else:
        cart_count = 0
        item_list = []
    # return HttpResponse(f"{cart_count}")
    return {"cart_count": cart_count}


def random_item(request):
    random_item = random.choice(list(Random.objects.all()))
    return {"random_item": random_item}


def delete(request, index):
    # print("index", index)
    # for item in enumerate(request.session["cart"]):
    # print(item[0] == [index])
    # if item[0] == index:
    # print(item)
    del request.session["cart"][index]
    request.session.modified = True
    return redirect("cart")


# def cart(request):
#     data = request.session.get("cart", [])
#     print("data", data)
#     items = []
#     if data:
#         for el in data:
#             obj = get_object_or_404(CartItem, id=el["cart_item"])
#             print("obj", obj)
#             items.append(obj)
#     print("ITEMS", items)
#     cart_sum = 0
#     for ci in items:
#         cart_sum = cart_sum + ci.pro_var_sum()
#     # print("cart_sum", cart_sum)
#     netto = cart_sum * 81 / 100
#     tax = cart_sum * 19 / 100

#     # if request.session.session_key:
#     #         print(Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key)
#     context = {
#         "cart_sum": cart_sum,
#         "netto": netto,
#         "tax": tax,
#         "items": items,
#     }
#     return render(request, "p1/cart.html", context)


# def checkout(request):
#     form = OrderForm()
#     data = request.session.get("cart", [])
#     print("data", data)
#     items = []
#     if data:
#         for el in data:
#             obj = get_object_or_404(CartItem, id=el["cart_item"])
#             print("obj", obj)
#             items.append(obj)
#     print("ITEMS", items)
#     cart_sum = 0
#     for ci in items:
#         cart_sum = cart_sum + ci.pro_var_sum()
#     print("cart_sum", cart_sum)
#     if request.session.session_key:
#         print(
#             Session.objects.get(pk=request.session.session_key).get_decoded(),
#             request.session.session_key,
#         )
#     return render(request, "p1/checkout.html", {"form": form})


# def printing(request):
#     if request.session.session_key:
#         print(
#             Session.objects.get(pk=request.session.session_key).get_decoded(),
#             request.session.session_key,
#         )
#     data = request.session.get("cart", [])
#     print("data", data)
#     items = []
#     if data:
#         for el in data:
#             obj = get_object_or_404(CartItem, id=el["cart_item"])
#             print("obj", obj)
#             items.append(obj)
#     print("ITEMS", items)
#     cart_sum = 0
#     for ci in items:
#         cart_sum = cart_sum + ci.pro_var_sum()
#     # print("cart_sum", cart_sum)
#     netto = cart_sum * 81 / 100
#     tax = cart_sum * 19 / 100

#     if request.method == "POST":
#         print(request.POST)
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         pickup_time = request.POST.get("pickup_time")
#         order = Order.objects.create(name=name, phone=phone, pickup_time=pickup_time)
#         # order.total = request.session
#         # Set the IP address of the printer
#         printer_ip = "192.168.178.177"
#         # Initialize the network connection to the printer
#         epson = Network(printer_ip)

#         # Send data to the printer
#         epson.text(f"{order.pickup_time}\n")
#         epson.text(f"{order.id}\n")
#         for el in data:
#             obj = get_object_or_404(CartItem, id=el["cart_item"])
#             print("obj", obj)
#             epson.text(f"{obj.product}\n")
#             for vl in obj.variations.all():
#                 epson.text(f"{vl}\n")

#         epson.cut()

#         # if order.daily_id.last() == None:
#         #     order.daily_id =1
#         # else:
#         #     order.daily_id = order.daily_id + 1
#         # order.save()
#         context = {"order": order}

#         # form = OrderForm(request.POST)
#         # if form.is_valid():

#         #     form.save(commit=False)

#         #     form.daily_id +=1
#         #     form.save()

#         #     print('DID', form.daily_id)
#         #     return HttpResponse('works')
#         # else:
#         #     return HttpResponse('error')
#         # pickup_time = request.POST.get('pickup_time')
#         # name = request.POST.get('name')
#         # tel = request.POST.get('phone')

#         # ! ganz am ende!!!!
#         # request.session.flush()
#     if request.method == "GET":
#         return redirect("failed")
#     return render(request, "p1/payment_success.html", context)


def payment_success(request):
    return HttpResponse("success")


def failed(request):
    return render(request, "p1/failed.html")

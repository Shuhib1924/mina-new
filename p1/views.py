from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import (
    Product,
    Variation,
    Category,
    Query,
    Notification,
    Screen,
    Random,
    Order,
)
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import json
import random
from pprint import pformat

import ast
from django.utils import timezone
from datetime import datetime, timedelta
import os
import time
from kafka import KafkaProducer


def notification(request):
    notifications = Notification.objects.filter(status=True)
    return {"notifications": notifications}


def home(request):
    screens = Screen.objects.order_by("rank")
    products = Product.objects.all().filter(active=True).order_by("-created_date")[:6]
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
    )
    # print("variations", variations)
    all_products = list(Product.objects.all())
    random_product = random.sample(all_products, min(4, len(all_products)))
    context = {
        "product": product,
        "queries": queries,
        "variations": variations,
        "random_product": random_product,
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
    cart_price = []
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
                    Variation,
                    id__in=item["item"][3]["variations"],
                )
            }
        except:
            variations = {"variations": ""}
        # print("Q - variations", variations)
        try:
            item_price = round(
                product["product"].price
                + sum([vp.price for vp in variations["variations"]]),
                2,
            )
        except:
            item_price = round(product["product"].price, 2)
        cart_price.append(item_price)
        # print("item_price", item_price)
        if not any("item_price" in el for el in item["item"]):
            item["item"].append({"item_price": float(item_price)})
        # item["item"].append({"item_price": float(item_price)})
        # print(item)
        cart_items.append(
            [user, product, queries, variations, {"item_price": item_price}]
        )
    # print(sum(cart_price))
    brutto = sum(cart_price)
    # print("brutto", brutto)
    netto = round(sum(cart_price) * 81 / 100, 2)
    # print("netto", netto)
    mwst = round(sum(cart_price) * 19 / 100, 2)
    # print("mwst", mwst)
    request.session["cart_price"] = {"brutto": float(brutto)}
    print('request.session["cart_price"]', request.session["cart_price"])
    request.session.modified = True
    # print("cart_items", cart_items)
    context = {
        "cart_items": cart_items,
        "brutto": brutto,
        "netto": netto,
        "mwst": mwst,
    }
    return render(request, "p1/cart.html", context)


def cart_count(request):
    try:
        cart_count = len(request.session["cart"])
    except:
        cart_count = 0
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


def checkout(request):
    try:
        brutto = request.session["cart_price"]["brutto"]
    except:
        brutto = 0
    return render(
        request,
        "p1/checkout.html",
        {"brutto": brutto},
    )


DATA_FILE = "p1/data.txt"


# Function to load the last daily_id and last_reset_date from the file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            daily_id = int(lines[0].strip()) if lines else 0
            last_reset_date_str = (
                lines[1].strip() if len(lines) > 1 else str(timezone.now().date())
            )
            last_reset_date = timezone.datetime.fromisoformat(
                last_reset_date_str
            ).date()
            return daily_id, last_reset_date
    return (
        0,
        timezone.now().date(),
    )  # Start from 0 and set last_reset_date to now if the file doesn't exist


# Function to save the current daily_id and last_reset_date to the file
def save_data(daily_id, last_reset_date):
    with open(DATA_FILE, "w") as file:
        file.write(f"{daily_id}\n")
        file.write(
            f"{last_reset_date.isoformat()}\n"
        )  # Save as ISO format for consistency


# Initialize daily_id and last_reset_date
daily_id, last_reset_date = load_data()

# daily_orders = []


def order(request):
    try:
        # data = json.loads(request.body)
        # transaction_data = data.get("transactionData", {})
        # # print("transaction_data", transaction_data)
        # form_data = data.get("formData", {})
        # # print("form_data", form_data)
        # # & create order_id
        # # global daily_id, daily_orders, last_reset_date
        # global daily_id, last_reset_date
        # # print(f"before: {daily_id} ")

        # # Use a fixed date for testing purposes
        # current_date = timezone.now().date()
        # # current_date = timezone.datetime(2024, 8, 3).date()
        # # print("current_date", current_date)

        # # Check if a new day has started
        # if current_date > last_reset_date:
        #     daily_id = 0
        #     # daily_orders = []  # Clear the list of orders
        #     last_reset_date = current_date  # Update last_reset_date to current date

        #     # print(f"after reset: {daily_id} ")
        # # else:
        # # print("no reset!")
        # # Save updated daily_id and last_reset_date
        # daily_id += 1
        # # daily_orders.append(daily_id)
        # save_data(daily_id, last_reset_date)
        # print(f"after process: {daily_id}")

        # # * 1. create order
        # order = Order(
        #     # ( transaction data
        #     daily_id=daily_id,
        #     orderID=transaction_data["orderID"],
        #     transactionID=transaction_data["transactionID"],
        #     paypal_total=float(
        #         transaction_data["purchase_units"][0]["amount"]["value"]
        #     ),
        #     href=transaction_data["links"][0]["href"],
        #     paypal_first_name=transaction_data["payer"]["name"]["given_name"],
        #     paypal_last_name=transaction_data["payer"]["name"]["surname"],
        #     paypal_email=transaction_data["payer"]["email_address"],
        #     paypal_id=transaction_data["payer"]["payer_id"],
        #     # ^ form data
        #     form_name=form_data["name"],
        #     form_pickup_time=form_data["pickupTime"],
        #     form_email=form_data["email"],
        #     form_phone=form_data["phone"],
        # ).save()
        # % 2. print receipt

        # 3. send email

        return JsonResponse({"success": "success"})
    except:
        if request.method == "POST":
            print(request.POST)
        return HttpResponse("NO JSON FOUND")


def success(request):
    producer = KafkaProducer(bootstrap_servers=["38.242.156.125:9092"], acks="all")
    test = "message"
    try:
        producer.send(
            "Mina",
            f"""[
                'date': {datetime.now()},
                'message':'message'
                ]""".encode(
                "utf-8"
            ),
        )
        time.sleep(0.1)
    except Exception as e:
        print(f"Transmission Error: {e}")
    return HttpResponse("success")


def g1(a):
    a += 1
    return a


def failed(request):
    x = 1
    x = g1(x)
    print("x", x)
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
                    Variation,
                    id__in=item["item"][3]["variations"],
                )
            }
        except:
            variations = {"variations": ""}
        # print("Q - variations", variations)
        try:
            item_price = round(
                product["product"].price
                + sum([vp.price for vp in variations["variations"]]),
                2,
            )
        except:
            item_price = round(product["product"].price, 2)
        str_product = product["product"].name
        print(f"""{user['user']}\n{str_product}""")
    return HttpResponse("failed")


# def printing(request):
#
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

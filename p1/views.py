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
from django.conf import settings
import ast
from django.utils import timezone
from datetime import datetime, timedelta
import os
import time
from kafka import KafkaProducer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from premailer import transform


def notification(request):
    notifications = Notification.objects.filter(status=True)
    return {"notifications": notifications}


def home(request):
    screens = Screen.objects.order_by("rank")
    latest_products = (
        Product.objects.all().filter(active=True).order_by("-created_date")[:4]
    )
    all_products = list(Product.objects.all().filter(active=True))
    random_products = random.sample(all_products, min(8, len(all_products)))
    context = {
        "latest_products": latest_products,
        "screens": screens,
        "random_products": random_products,
    }

    return render(request, "p1/index.html", context)


def category(request, cslug):
    category = Category.objects.get(slug=cslug)
    products = Product.objects.filter(category=category).order_by("rank")
    product_count = products.count()
    context = {
        "category": category,
        "products": products,
        "product_count": product_count,
    }
    return render(request, "p1/category.html", context)


def all_categories(request):
    all_categories = Category.objects.all().filter(active=True).order_by("rank")
    return {"all_categories": all_categories}


def detail(request, cslug, pslug):
    category = Category.objects.get(slug=cslug)
    product = Product.objects.get(slug=pslug)
    # print("product", product)
    queries = (
        Query.objects.filter(product_query__name=product.name)
        .filter(active=True)
        .order_by("rank")
    )
    # print("queries", queries)
    variations = Variation.objects.filter(
        query_variation__name__in=[i.name for i in queries]
    ).order_by("rank")
    # print("variations", variations)
    all_products = list(Product.objects.all().filter(active=True))
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


def menu(request, cslug, pslug):
    category = Category.objects.get(slug=cslug)
    product = Product.objects.get(slug=pslug)
    # print("product", product)
    queries = Query.objects.filter(product_query__name=product.name).order_by("rank")
    # print("queries", queries)
    variations = Variation.objects.filter(
        query_variation__name__in=[i.name for i in queries]
    ).order_by("rank")
    # print("variations", variations)
    all_products = list(Product.objects.all().filter(active=True))
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
    return render(request, "p1/menu.html", context)


def cart(request):
    # #check cart
    cart_session = request.session.get("cart")
    if not cart_session:
        cart_session = request.session.create()
        cart_session = request.session["cart"] = []

    if request.method == "POST":
        print(request.POST)
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
    # print('request.session["cart_price"]', request.session["cart_price"])
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
        data = json.loads(request.body)
        # print("data", data)
        transaction_data = data.get("transactionData", {})
        # print("transaction_data", transaction_data)
        form_data = data.get("formData", {})
        # print("form_data", form_data)
        # & create order_id
        # global daily_id, daily_orders, last_reset_date
        global daily_id, last_reset_date
        # print(f"daily_id before: {daily_id} ")

        # Use a fixed date for testing purposes
        current_date = timezone.now().date()
        # current_date = timezone.datetime(2024, 8, 3).date()
        # print("current_date", current_date)

        # Check if a new day has started
        if current_date > last_reset_date:
            daily_id = 0
            # daily_orders = []  # Clear the list of orders
            last_reset_date = current_date  # Update last_reset_date to current date

            # print(f"after reset: {daily_id} ")
        # else:
        # print("no reset!")
        # Save updated daily_id and last_reset_date
        daily_id += 1
        # daily_orders.append(daily_id)
        save_data(daily_id, last_reset_date)
        # print(f"daily_id after process: {daily_id}")

        # * 1. create order
        order = Order(
            # ( transaction data
            daily_id=daily_id,
            orderID=transaction_data["orderID"],
            transactionID=transaction_data["id"],
            paymentCaptureID=transaction_data["purchase_units"][0]["payments"]["captures"][0]["id"],
            paypal_total=float(
                transaction_data["purchase_units"][0]["amount"]["value"]
            ),
            href=transaction_data["links"][0]["href"],
            paypal_first_name=transaction_data["payer"]["name"]["given_name"],
            paypal_last_name=transaction_data["payer"]["name"]["surname"],
            paypal_email=transaction_data["payer"]["email_address"],
            # paypal_email=transaction_data["payer"]["phone"],
            paypal_id=transaction_data["payer"]["payer_id"],
            # ^ form data
            form_pickup_time=form_data["pickupTime"],
            form_phone=form_data["phone"],
            form_companyName=form_data["companyName"],
            form_companyAddress=form_data["companyAddress"],
            form_companyZip=form_data["companyZip"],
            form_companyCity=form_data["companyCity"],
            form_companyUst=form_data["companyUst"],
        )
        print("1. order created")
        # $ it's not saved yet see below!
        # % 2. print receipt
        try:
            collected_order = []
            form_data_order = {
                "pickupTime": f"{form_data['pickupTime']}",
                "daily_id" : f"{daily_id}",
                "currentTime": f"{datetime.now().strftime('%H:%M:%S')}",
                "first_name": f"{transaction_data['payer']['name']['given_name']}",
                "last_name": f"{transaction_data['payer']['name']['surname']}",
                "phone": f"{form_data['phone']}",
            }
            # & it's NOT saved yet!
            collected_order.append({"form_data": form_data_order})
            order_products = []
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
                query_set = []
                for q in queries["queries"]:
                    # print(q.query_variation.all())
                    variation_set = [
                        v for v in variations["variations"] if v in q.query_variation.all()
                    ]
                    # print("variation_set", variation_set)
                    query_set.append(
                        {
                            "query": q.name,
                            "variation_set": [v.name for v in variation_set],
                        }
                    )
                order_item = {
                    "user": user["user"],
                    "product": product["product"].name,
                    "query_set": query_set,
                }
                order_products.append(order_item)
            collected_order.append({"products": order_products})
            # print(collected_order)
            json_order = {"order": collected_order}
            # print(json.dumps(json_order, indent=4))
            order.order_data = json.dumps(json_order, indent=4)
            order.paypal_data = json.dumps(data, indent=4)
            meta_dict = {}
            for key, value in request.META.items():
                try:
                    json.dumps({key: value})  # Try to serialize the key-value pair
                    meta_dict[key] = value
                except (TypeError, ValueError):
                    meta_dict[key] = str(value)  # Convert non-serializable objects to strings
            # Convert the filtered dictionary to a JSON string
            meta_json = json.dumps(meta_dict)
            # print("meta_json", meta_json)
            order.request_meta = json.dumps(meta_json)
            order.save()
            print("1.1. order added json")
        #     # ^ sending print data
            producer = KafkaProducer(
                bootstrap_servers=["38.242.156.125:9092"],
                acks="all",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            producer.send("Mina", value=json_order)
            producer.flush()
            producer.close()
        except Exception as e:
            print(f'printing error from server: {e}')
        print("2. printing done")
        # ~ 3. send email
        email = transaction_data["payer"]["email_address"]
        # email = 'shuhib_s@live.de' # % for development
        subject = f"Lassen Sie es sich schmecken, Ihre Bestellnummer lautet Nr. {daily_id}"

        cart_items = []
        cart_price = []
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
        # print(cart_items)
        cart_price = float(request.session["cart_price"]["brutto"])
        context = {
            "date": datetime.now().date,
            "daily_id": daily_id,
            "pickup": form_data["pickupTime"],
            "email": email,
            "subject": subject,

            "payer_id": transaction_data["payer"]["payer_id"],
            "first_name": transaction_data["payer"]["name"]["given_name"],
            "last_name": transaction_data["payer"]["name"]["surname"],
            "transaction_id": transaction_data["id"],

            "company_name": form_data["companyName"],
            "company_address": form_data["companyAddress"],
            "company_zip": form_data["companyZip"],
            "company_city": form_data["companyCity"],
            "company_ust": form_data["companyUst"],

            "capture_id": transaction_data["purchase_units"][0]["payments"]["captures"][0]["id"],
            "cart_items": cart_items,
            "brutto": brutto,
            "netto": netto,
            "mwst": mwst,
        }
        # print("cart_items", cart_items)

        html_content = render_to_string("p1/email/invoice.html", context)

        # Use premailer to inline the CSS
        inlined_html = transform(html_content)

        # Create plain text version
        text_content = strip_tags(inlined_html)

        # Create the email
        email = EmailMultiAlternatives(
            subject, text_content, settings.EMAIL_HOST_USER, [email]
        )
        email.attach_alternative(inlined_html, "text/html")
        email.send()
        print('3. email sended')
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"Error": "From Server, No JSON Foundable"})


def success(request):
    last_order = Order.objects.latest('id')
    request.session.flush()
    return render(request, 'p1/success.html', {'last_order': last_order})


def failed(request):
    # print(json.dumps(data, indent=4))
    print(request.META)
    return render(request, 'p1/failed.html')


def email(request):
    # # ~ get data
    # data = """{"transactionData": {"orderID": "52678863VG386592F", "id": "52678863VG386592F", "status": "COMPLETED", "intent": "CAPTURE", "create_time": "2024-08-05T18:47:51Z", "update_time": "2024-08-05T18:47:58Z", "payer": {"name": {"given_name": "Buyer", "surname": "Buyer"}, "email_address": "buyer@speed.codes", "payer_id": "56NTW9BN78UR8", "address": {"country_code": "DE"}, "phone": null}, "purchase_units": [{"reference_id": "default", "amount": {"currency_code": "EUR", "value": "7.00"}, "payee": {"email_address": "seller@speed.codes", "merchant_id": "R9EVPB7E2LKPN"}, "shipping": {"name": {"full_name": "Buyer Buyer"}, "address": {"address_line_1": "Badensche Str. 24", "admin_area_2": "Berlin", "admin_area_1": "Berlin", "postal_code": "10715", "country_code": "DE"}}, "payments": {"captures": [{"id": "2KB24524XU2537004", "status": "COMPLETED", "amount": {"currency_code": "EUR", "value": "7.00"}, "final_capture": true, "seller_protection": {"status": "ELIGIBLE", "dispute_categories": ["ITEM_NOT_RECEIVED", "UNAUTHORIZED_TRANSACTION"]}, "create_time": "2024-08-05T18:47:58Z", "update_time": "2024-08-05T18:47:58Z"}]}}], "links": [{"href": "https://api.sandbox.paypal.com/v2/checkout/orders/52678863VG386592F", "rel": "self", "method": "GET"}]}, "formData": {"pickupTime": "10:12", "phone": "", "term": "true", "companyName": "Speed.Codes", "companyAddress": "Adenauerallee 18", "companyZip": "20097", "companyCity": "Hamburg", "companyUst": "DE123435343"}}"""
    # parsed_data = json.loads(data)
    # print("parsed_data", parsed_data)

    # transaction_data = parsed_data['transactionData']
    # print("transaction_data", transaction_data)
    # form_data = parsed_data['formData']
    # print("form_data", form_data)



    return render(request, "p1/email/invoice.html", context)


def impressum(request):
    # return HttpResponse("test")
    return render(request, "p1/impressum.html")


def datenschutz(request):
    # return HttpResponse("test")
    return render(request, "p1/datenschutz.html")


def agb(request):
    # return HttpResponse("test")
    return render(request, "p1/agb.html")


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

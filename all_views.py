from django.shortcuts import render, redirect
from .models import Product, Variation, CartItem
from django.utils.crypto import get_random_string
# Create your views here.



# def create_order(request, product_id):
#     if request.method == "POST":
#         # Create Kafka producer to send message
#         # producer = KafkaProducer(bootstrap_servers="38.242.156.125:9092")

#         product = Product.objects.get(id=product_id)
#         order_variations = request.POST.getlist("variations")

#         # Print order details to Epson printer
#         # printer_ip = "192.168.178.177"
#         # printer = Network(printer_ip, port=9100)

#         # printer.text(f"{product.name}\n")

#         # for variation_id in order_variations:
#         #     variation = Variation.objects.get(id=variation_id)
#         #     # Print variation details
#         #     printer.text(f"- {variation.name}\n")

#         #     # Send variation details to Kafka topic
#         #     producer.send("Ahmad123", value=str(variation).encode("utf-8"))

#         # # Close the printer connection and Kafka producer
#         # printer.cut()
#         # producer.close()

#         return redirect("order", id=product_id)
#     else:
#         product = Product.objects.get(id=product_id)
#         return render(request, "order.html", {"product": product})





    # unique_id = get_random_string(length=32)
    # print("unique_id", unique_id)
    # request.session[unique_id] = [1,2,3]
    # print("request.session[unique_id]", request.session[unique_id])

    # print("session", session)
    # session[unique_id]= [1,2,3]
    # cart = session.get(unique_id)
    # if "session_key" not in request.session:
    #     cart = session["session_key"] = {}
    # session.cart = cart
    # print("session.cart = cart", session.cart)





from django.shortcuts import render
from .models import Category, Product, Variation, Order
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.http import require_http_methods



@require_http_methods(['POST'])
def update(request, id):
    # if not request.session.get('cart'):
    #     request.session['cart']=[id]
    # else:
    #     request.session['cart'].append(id)
    if not request.session.get("cart"):
        request.session["cart"] = []
    request.session["cart"].append(id)

    # print(request.session.get('cart'))
    print(json.loads(request.body))
    # print(request.session)
    list = []
    product = Product.objects.get(id=id)
    if request.method == "POST":
        # print(json.loads(request.body))
        list.append({"product_id": id})
        return JsonResponse(list, safe=False)
    else:
        return JsonResponse('error to add')


def checkout(request):
    product_ids = request.session["cart"]
    selected = Product.objects.filter(id__in=product_ids)

    return HttpResponse(f'{selected}')

# def add_cart(request):
#     if request.method == 'POST':
#         print('TEST')
#         cart_list = {}
#         print("cart_list", cart_list)
#         product = Product.objects.get(id=id)
#         cart_list.add(product)
#         cart_session = request.session.session_key
#         if cart_session:
#             print("get session", cart_session)
#         else:
#             cart_session = request.session.create()
#             print("created", cart_session)
#         return JsonResponse({})







def example(request):
    return render(request, 'h1-example.html')

def save_variations_to_session(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        variation_ids = request.POST.getlist('variation_ids[]')

        product = get_object_or_404(Product, id=product_id)
        variations = Variation.objects.filter(id__in=variation_ids)

        # Retrieve existing variations from session
        selected_variations = request.session.get('selected_variations', [])

        # Convert the list of variation ids to a set for quick lookup
        existing_variation_ids = {v['id'] for v in selected_variations}

        # Append new variations to the session list
        for variation in variations:
            if variation.id not in existing_variation_ids:
                selected_variations.append({
                    'id': variation.id,
                    'name': variation.name,
                    'price': str(variation.price)  # Convert Decimal to string
                })

        # Update the session with the new list of variations
        request.session['selected_variations'] = selected_variations

        return redirect('list_variations')
    return HttpResponseBadRequest('Invalid request method.')

def list_variations_from_session(request):
    try:
        print(Session.objects.get(pk=request.session.session_key).get_decoded())
    except Session.DoesNotExist:
        pass
    selected_variations = request.session.get('selected_variations', [])
    # print('decoded: ', sk.get_decoded())
    # for selected in selected_variations:
        # pass
    return render(request, 'h1-list1.html', {'selected_variations': selected_variations})

def delete_variation_from_session(request, variation_id):
    selected_variations = request.session.get('selected_variations', [])
    updated_variations = [v for v in selected_variations if v['id'] != variation_id]
    request.session['selected_variations'] = updated_variations
    return redirect('list_variations')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'h1-req1.html', {'product': product})

def session1(request):
    sk = Session.objects.get(pk="hnv777pyq2u2b6r5x6v60h9wbei77p8e")
    [print(f"all: Key: {key}, Value: {value}") for key, value in request.session.items()]
    visits = request.session.get('num', 0)
    print('after set',visits)
    visits +=1
    print('after',visits)
    request.session['num'] = visits
    print('decoded: ', sk.get_decoded())
    if visits > 4 : del(request.session['num'])
    return HttpResponse(f'counter: {visits}')


def add2(request, pid):
    product = get_object_or_404(Product, id=pid)

# def list2(request):





from .models import Product
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def list(request):
    products = Product.objects.all()
    return render(request, 't1/list.html', {'products':products})

def detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 't1/detail.html', {'product':product})

# def add_cart():


# def product(request, id):
#     product = Product.objects.get(id=id)
#     return render(request, 'product.html', {'product':product})

# def add_to_cart(request):
#     if request.method == 'POST':
#         selected_fields = request.POST.getlist('selected_fields[]')
#         request.session['cart_items'] = selected_fields
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})

# def cart(request):
#     cart_items = request.session.get('cart_items', [])
#     products_in_cart = Product.objects.filter(id__in=cart_items)
#     return render(request, 'cart.html', {'products_in_cart': products_in_cart})

@csrf_exempt
def save_request(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        variations = request.POST.getlist('variations')
        quantity = request.POST.get('quantity')

        # Save data to session
        request.session['product_name'] = product_name
        request.session['variations'] = variations
        request.session['quantity'] = quantity

        return JsonResponse({'message': 'Request saved in session'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
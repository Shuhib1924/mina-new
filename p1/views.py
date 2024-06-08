from math import e
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import Product, Variation, Category, CartItem
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
import json

def home(request):
    products = Product.objects.all().order_by('-created_date')[:4]
    categories = Category.objects.all()
    context= {
        'products':products,
        'categories':categories,
    }
    return render(request, 'p1/index.html', context)

def all_categories(request):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}

def category(request, cid):
    category = Category.objects.get(id=cid)
    return render(request,'p1/category.html', {'category':category})

def listing_product(request):
    products = Product.objects.all()
    return render(request, 'p1/list.html', {'products': products})


def listing_product(request):
    products = Product.objects.all()
    return render(request, 'p1/list.html', {'products': products})

def detail(request, pid):
    if request.session.session_key:
        print(Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key)
    product = Product.objects.get(id=pid)
    context = {
        'product':product,
    }
    # return HttpResponse(f"{product.name}")
    return render(request, 'p1/detail.html', context)

def add_cart(request):
    # *get or create session
    cart_session = request.session.get('cart')
    if not cart_session:
        cart_session=request.session.create()
        cart_session = request.session['cart']=[]

    print("cart_session", cart_session)
    # %2. selected product from request
    # cart_list = []
    if request.method == "POST":
        # $ check post request
        # print("post", request.POST, '\n')
        # * get product
        get_product_id = request.POST.get('product')
        selected_product = get_object_or_404(Product, id=get_product_id)
        print("selected_product", selected_product,'\n')
        # cart_session.append(selected_product)
        # request.session['cart']= cart

        get_variation_list = request.POST.getlist('variations[]')
        selected_variations = []
        for vid in get_variation_list:
            variation= get_object_or_404(Variation, id=vid)
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

        #  add into cart and save it into session
        cart_session.append({'cart_item': cart_item.id})
        request.session['cart']= cart_session
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
    return JsonResponse({'message': 'success'})


def cart(request):
    data = request.session.get('cart', [])
    print("data", data)
    items = []
    if data:
        for el in data:
            obj = get_object_or_404(CartItem, id=el['cart_item'])
            print("obj", obj)
            items.append(obj)
    print(items)

    # if request.session.session_key:
    #         print(Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key)
    return render(request, 'p1/cart.html', {'items':items})

# def cart(request):
#     data = request.session.get('cart', [])
#     items = []
#     if data:
#         for el in data:
#             obj = get_object_or_404(CartItem, id=el['cart_item'])
#             selected_variations = obj.variations.all()
#             items.append({
#                 'cart_item': obj,
#                 'selected_variations': selected_variations
#             })

#     return render(request, 'p1/cart.html', {'items': items})

def delete_item(request, id):
    item = get_object_or_404(CartItem, id=id)
    sk = request.session.session_key
    objects = Session.objects.get(pk=request.session.session_key).get_decoded()
    cart = request.session.get('cart', [])
    print("cart", cart, '\n')
    # delete from session
    for i in cart:
        if i['cart_item']==id:
            cart.remove(i)
    print(cart)
    # save it into session
    request.session['cart']=cart
    # delete from db
    item.delete()
    # return HttpResponse(f'CartItem ID: {item.id}<hr>Product: {item.product.name} <hr> items count: {len(cart)}<hr> key: {sk} <hr> all objects: {objects}<hr>')
    return redirect('cart')
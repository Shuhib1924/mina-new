from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token

from .models import Product, CartItem
from django.contrib.sessions.models import Session

def product_list(request):
    try:
        print(Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key)
    except:
        pass
    products = Product.objects.all()
    return render(request, 't1/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    if request.method == "POST":
        # create or get sessions
        cart = request.session.get('cart_test')
        print("get cart", cart)
        if not cart:
            cart = request.session.create()
            cart = request.session.get('cart_test', [])
        # print("after create", cart)

        # see all objects in django session
        if request.session.session_key:
            print(Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key)

        # get product
        product = get_object_or_404(Product, id=product_id)
        # set object to cart_item
        cart_item = CartItem(product=product)
        cart_item.save()
        # add into session
        cart.append({'product': cart_item.id})
        # save into session
        request.session['cart_test'] = cart
        return JsonResponse({'status': "success"})
        return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart_test', [])
    if request.session.session_key:
            print(Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key)
    cart_items = []
    # print("cart", cart)
    if cart:
        cart_items = [get_object_or_404(CartItem, id=cart_id['product']) for cart_id in cart]

    print("after loop", cart_items)

    return render(request, 't1/cart.html', {'cart_items': cart_items})

def delete_item(request, id):
    item = get_object_or_404(CartItem, id=id)
    sk = request.session.session_key
    objects = Session.objects.get(pk=request.session.session_key).get_decoded()
    cart = request.session.get('cart_test', [])
    print("cart", cart, '\n')
    # delete from session
    for i in cart:
        if i['product']==id:
            cart.remove(i)
    print(cart)
    # save it into session
    request.session['cart_test']=cart
    # delete from db
    item.delete()
    # return HttpResponse(f'CartItem ID: {item.id}<hr>Product: {item.product.name} <hr> items count: {len(cart)}<hr> key: {sk} <hr> all objects: {objects}<hr>')
    return redirect('cart_view')

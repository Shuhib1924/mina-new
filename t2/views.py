from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from .models import Product, ProductVariation
from django.contrib.sessions.models import Session
from django.http import HttpResponse

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def add_to_cart(request):

    # create or get session = []
    cart_key = request.session.session_key
    if not request.session.session_key:
        cart_key = request.session.create()
        cart_key = request.session['cart_t2']= []
    get_cart_session = request.session.get('cart_t2', [])
    print("get_cart_session", get_cart_session)

    if request.method == 'POST':
        get_product = request.POST.get('product_id')
        get_variation_list = request.POST.getlist('variations')

        product = get_object_or_404(Product, pk=get_product)

        for variation_id in get_variation_list:
            variation = get_object_or_404(ProductVariation, pk=variation_id)
            variation.is_selected = True
            variation.save()



        # Add the product_id and selected variation_ids to session for cart
        get_cart_session.append({'product_id': get_product, 'variations': get_variation_list})
        request.session['cart_t2']= get_cart_session
        print("after ADD", request.session.get('cart_t2', []))

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def cart(request):
    # print(request.session.get('cart_t2'))
    try:
        print(Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key)
    except:
        pass
    cart_data = request.session.get('cart_t2', [])
    # print("CALL LIST", cart_data)
    cart_contents = []

    for item in cart_data:
        product_id = item.get('product_id')
        print("product_id", product_id)
        variations_selected = item.get('variations', [])
        print("variations_selected", variations_selected)

        product = get_object_or_404(Product, id=product_id)
        variations = ProductVariation.objects.filter(product=product, id__in=variations_selected)

        cart_contents.append({'product': product, 'variations': variations})
        print("cart_contentsFINAL", request.session['cart_t2'])
    context = {
        'cart_contents': cart_contents,
        # 'product': product,
        # 'variations': variations,
        }
    return render(request, 'cart.html', context)

def test(request):
    get_t1 = request.session.session_key
    if not get_t1:
        request.session.create()
        request.session['t1']=[]
    get_t1 = request.session.get('t1', [])

    get_t1.append({'a1':1})
    request.session['t1'] = get_t1
    print("get_t1", get_t1)

    sk = Session.objects.get(pk=request.session.session_key).get_decoded(), request.session.session_key
    return HttpResponse(f'{sk}<hr>{get_t1}')


def delete_session(request):

    request.session.flush()

    return redirect('cart2')
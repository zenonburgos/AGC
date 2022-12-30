import math
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from core.store.context_processors import get_cart_counter, get_cart_amounts
from core.inv.models import Category, Product

from .models import Cart


def store(request, category_slug=None, group_slug=None):      
    categories = None
    groups = None
    products = None

    if category_slug != None:
         categories = get_object_or_404(Category, slug=category_slug)
     #     products = Product.objects.filter(category__parent=categories, store=True)
         products = Product.objects.filter(category=categories, store=True)
         paginator = Paginator(products, 10)
         page = request.GET.get('page')
         paged_products = paginator.get_page(page)

         product_count = products.count()
    else:
         products = Product.objects.all().filter(store=True)
         paginator = Paginator(products, 20)
         page = request.GET.get('page')
         paged_products = paginator.get_page(page)
        #  print(paged_products.has_other_pages)
         product_count = products.count()

#    print("estos son los productos del slug", category_slug, products)
#     if group_slug != None:
#          groups = get_object_or_404(Group, slug=group_slug)
#          products = Product.objects.filter(group=groups, store=True)
#          product_count = products.count()
#     else:
#          products = Product.objects.all().filter(store=True)
#          product_count = products.count()         
#          print(group_slug)

#     category = get_object_or_404(Category, slug=category_slug)
#     products = category.products.filter(store=True)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = []
        
    context = {
     #     'category': category,
         'products': paged_products,
         'product_count': product_count,
         'cart_items': cart_items,
    }
    
    return render(request, 'store/store.html', context)


class MyCount(object):
    def __init__(self):
        self.v1 = 0
        self.v2 = 1
    def bump(self):
        self.v1 += 1
        self.v2 = self.v1 + 1
        return ''


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        strikePrice = single_product.price + ((single_product.price/100)*20)

        offers = Product.objects.all().filter(store=True, special_offers=True).order_by('-created_at')
        offersCount = Product.objects.filter(store=True, special_offers=True).count()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
       
    context = {
        'single_product': single_product,
        'strikePrice': strikePrice,
        'offers': offers,
        'range': range(math.ceil(offersCount)),
        'contador': MyCount(),
        'cart_items': cart_items,
    }
    return render(request, 'store/product_detail.html', context)


def add_to_cart_in_product_detail(request, producto_id):
    product_qty = int(request.GET['product_qty'])
    # print(product_qty)
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the product exists
            try:
                producto = Product.objects.get(id=producto_id)
                
                # check if the user has already added that product to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, product=producto)

                    # Increase the cart quantity
                    
                    chkCart.quantity += product_qty
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Cantidad de producto incrementada en carrito.', 
                    'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity,
                    'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, product=producto, quantity=product_qty)
                    return JsonResponse({'status': 'Success', 'message': 'Producto agregado al carrito.', 
                    'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity,
                    'cart_amount': get_cart_amounts(request)})
                    print(cart_amount)
            except:
                # print(chkCart)
                return JsonResponse({'status': 'Failed', 'message': 'Este producto no existe.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Solicitud inválida.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Por favor regístrese o ingrese al sistema...'})


def add_to_cart(request, producto_id):    
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the product exists
            try:
                producto = Product.objects.get(id=producto_id)
                
                # check if the user has already added that product to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, product=producto)

                    # Increase the cart quantity
                    
                    chkCart.quantity += 1                    
                    chkCart.save()
                    
                    pricecart = chkCart.quantity * chkCart.product.price

                    return JsonResponse({'status': 'Success', 'message': 'Cantidad de producto incrementada en carrito.', 
                    'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'pricecart': pricecart,
                    'cart_amount': get_cart_amounts(request)})
                except: # Si no se ha agregado previamente ningún producto al carrito
                    chkCart = Cart.objects.create(user=request.user, product=producto, quantity=1)
                    
                    return JsonResponse({'status': 'Success', 'message': 'Producto agregado al carrito.', 
                    'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity,
                    'cart_amount': get_cart_amounts(request)})
            except:
                # print(chkCart)
                return JsonResponse({'status': 'Failed', 'message': 'Este producto no existe.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Solicitud inválida.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Por favor regístrese o ingrese al sistema...'})


def decrease_cart(request, producto_id):    
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the product exists
            try:
                producto = Product.objects.get(id=producto_id)
                
                # check if the user has already added that product to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, product=producto)                    
                    
                    if chkCart.quantity > 1:
                        # Decrease the cart quantity                    
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    
                    pricecart = chkCart.quantity * chkCart.product.price

                    return JsonResponse({'status': 'Success', 
                    'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'pricecart': pricecart,
                    'cart_amount': get_cart_amounts(request)})
                except:                    
                    return JsonResponse({'status': 'Failed', 'message': 'No tiene este producto en su carrito.'})
            except:
                # print(chkCart)
                return JsonResponse({'status': 'Failed', 'message': 'Este producto no existe.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Solicitud inválida.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Por favor regístrese o ingrese al sistema...'})


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
        
    context = {
        'cart_items': cart_items,    
    }
    
    return render(request, 'store/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Item eliminado.', 
                    'cart_counter': get_cart_counter(request),
                    'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Item no existe.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Solicitud inválida.'})

def search(request):
    if 'keyword' in request.GET:
        products = ""    
        product_count = 0
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_at').filter(Q(description__icontains=keyword) | 
                                                                     Q(name__icontains=keyword) | 
                                                                     Q(code__icontains=keyword) |
                                                                     Q(model__icontains=keyword) |
                                                                     Q(tags__icontains=keyword))
            if 'keyword' in request.GET and request.GET['keyword']:
                page = request.GET.get('page')
                keyword = request.GET['keyword']
                paginator = Paginator(products, 15)
            paged_products = paginator.get_page(page)
            product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
import math
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from core.inv.models import Product
from core.store.models import Cart


class MyCount(object):
    def __init__(self):
        self.v1 = 0
        self.v2 = 3
    def bump(self):
        self.v1 += 3
        self.v2 = self.v1 + 3
        return ''

# @login_required
def IndexView(request):
    products = Product.objects.all().filter(store=True).order_by('-created_at')
    offers = Product.objects.all().filter(store=True, special_offers=True).order_by('-created_at')
    featured = Product.objects.all().filter(store=True, featured_products=True).order_by('-created_at')
    bestseller = Product.objects.all().filter(store=True, best_seller=True).order_by('-created_at')
    offersCount = Product.objects.filter(store=True, special_offers=True).count()    
    # print(products)
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    else:
        cart_items = []
    
    # print(products)
    # print(math.ceil(offersCount/3))      
    context = {
        'products': products,
        'offers': offers,
        'featured': featured,
        'bestseller': bestseller,
        'range': range(math.ceil(offersCount/3)),
        'contador': MyCount(),
        'cart_items': cart_items,    
        
    }
    return render(request, 'index.html', context)
### PRUEBAS CON SCRIPTS
# name = "Plancha para pupusas de 1.30"
# words = name.split()

# order_name = words[0]

# print(order_name)
######################################

import decimal
import os

import sys

## Para que funcione debe entrar a core/inv y correr python ../../manage.py test ...
## (Sí, justo en singular y sin extensión).
sys.path.append('../../')
from config.wsgi import *

from core.inv.models import Product

products = Product.objects.all()

xcode = 1
for product in products:
    # nombre = product.name
    # words = product.name.split()
    # # word2 = product.name.split()[1]
    # # word3 = product.name.split()[2]

    # name_1words = " ".join(words[0:1])
    # name_2words = " ".join(words[0:2])
    # name_3words = " ".join(words[0:3])
    # name_4words = " ".join(words[0:4])

    # # if 'LED' in words:
    # #     product.product_type = name_2words        
    # # print(words)

    # product.name = nombre.title()
    # product.store = False
    # product.slug = str(xcode)
    # product.code = str(xcode)
    # product.model = str(xcode)
    # product.code = product.barcode
    # product.model = product.barcode
    product.cost = float(product.cost)/1.13
    xcode += 1
    print(product.name)

    product.save()




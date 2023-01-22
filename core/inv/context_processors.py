from django.db.models import Q
from core.inv.models import Category, Group, Branch


def menu_categories(request):
    categories = Category.objects.filter(parent=None)
    
    return {'menu_categories': categories}


#Esto filtra los productos directamente por su categoría padre
#Aún no lo ocupo
def menu_subcategories(request):
    subcategories = Category.objects.filter(parent__isnull=False)

    return {'submenu_categories': subcategories}


def menu_almacenes(request):
    almacenes = Branch.objects.all
    print(almacenes)
    return {'almacenes': almacenes}







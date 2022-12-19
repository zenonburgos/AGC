from datetime import datetime

# from config.settings import MEDIA_URL, STATIC_URL
from decimal import Decimal
import uuid


from click.core import F
from crum import get_current_user
from django.db.models import Sum
from django.db.models.functions import Coalesce

from config.settings import AUTH_USER_MODEL

from config import settings
from django.db import models
from django.forms import model_to_dict, FloatField

from core.inv.choices import gender_choices
from core.models import BaseModel

from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse

class Category(BaseModel):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='category/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.created_by = user
            else:
                self.updated_by = user
        super(Category, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item
    
    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
        
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])


def set_slug(sender, instance, *args, **kwargs): #callback
    instance.slug = slugify(instance.name)

pre_save.connect(set_slug, sender=Category)


class Group(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,verbose_name='Categoría')
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='group/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.created_by = user
            else:
                self.updated_by = user
        super(Group, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item
    
    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']
    
    def get_url(self):
        return reverse('products_by_group ', args=[self.slug])
    

def set_slug(sender, instance, *args, **kwargs): #callback
    instance.slug = slugify(instance.name)


pre_save.connect(set_slug, sender=Group)


class Brand(BaseModel):
    name  = models.CharField(max_length=100, unique=True, verbose_name="Marca")
    slug = models.SlugField(null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='brand/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.upper()
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.created_by = user
            else:
                self.updated_by = user
        super(Brand, self).save()
    
    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item
    
    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['name']

def set_slug(sender, instance, *args, **kwargs): #callback
    instance.slug = slugify(instance.name)

pre_save.connect(set_slug, sender=Brand)


class Product(BaseModel):
    code = models.CharField(max_length=20,unique=True, verbose_name='Código interno')
    barcode = models.CharField(max_length=50, null=True, blank=True, verbose_name='Código barra')
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción detallada')
    slug = models.SlugField(max_length=150, null=True, blank=True, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True,verbose_name='Categoría')
    product_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='Tipo de producto')
    model = models.CharField(max_length=50, null=True, blank=True, verbose_name='Modelo')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True,verbose_name='Marca')
    marca = models.CharField(max_length=50, null=True, blank=True, verbose_name='Marca')
    cost = models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2, null=True, blank=True, verbose_name='Costo')
    fact = models.FloatField(default=0.58, null=True, blank=True, verbose_name='Factor')
    price = models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2, null=True, blank=True, verbose_name='Precio venta')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0, null=True, blank=True, verbose_name='Stock')

    # fixed_price = models.BooleanField(default=True, verbose_name='Fijar precio')
    fact2 = models.FloatField(default=0.65, null=True, blank=True, verbose_name='Factor 2')
    fact3 = models.FloatField(default=0.70, null=True, blank=True, verbose_name='Factor 3')
    price2 = models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2, null=True, blank=True, verbose_name='Precio 2')
    price3 = models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2, null=True, blank=True, verbose_name='Precio 3')
    tags = models.CharField(max_length=150, null=True, blank=True, verbose_name='Palabras clave')
    last_purchase_date = models.DateField(null=True, blank=True, verbose_name='Ult. fecha compra')
    is_inventoried = models.BooleanField(default=True, verbose_name='¿Es inventariado?')
    active = models.BooleanField(default=True, verbose_name='Activo')
    catalogue = models.BooleanField(default=True, verbose_name='Catálogo')
    store = models.BooleanField(default=False, verbose_name='webstore')

    special_offers = models.BooleanField(default=False, verbose_name='Ofertas')
    featured_products = models.BooleanField(default=False, verbose_name='Destacados')
    best_seller = models.BooleanField(default=False, verbose_name='Más vendidos')
    is_hot = models.BooleanField(default=False, verbose_name='Hot')

    def __str__(self):
        # return f'{self.name} ({self.category.name})'
        return f'{self.name}'
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # self.name = self.name.upper()
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.created_by = user
            else:
                self.updated_by = user
        super(Product, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        item['category'] = self.category.toJSON()
        item['brand'] = self.brand.toJSON()
        # item['group'] = self.group.toJSON()
        item['image'] = self.get_image()
        item['price'] = f'{self.price:.2f}'
        return item

    def get_image(self):        
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['product_type']
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

def generate_slug(string):
    id = str(uuid.uuid4())
    return slugify('{}-{}'.format(
        string, id[:8]
    ))

def set_slug(sender, instance, *args, **kwargs):  # callback
    if instance.slug:
        return

    slug = generate_slug(instance.name)

    while(Product.objects.filter(slug=slug).exists()):
        slug = generate_slug(instance.name)
    
    instance.slug = slug


pre_save.connect(set_slug, sender=Product)


class Client(BaseModel):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name='Dni')
    date_of_birth = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} {self.surnames} ({self.dni})'

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_of_birth'] = self.date_of_birth.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Supplier(BaseModel):
    nrc = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name='NRC')
    razon_social = models.CharField(max_length=150, null=True, blank=True, verbose_name='Razón Social')
    nit = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='NIT')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        # if self.name != "" and self.name != "":
        #     return f'{self.name} {self.surname}'
        # else:
        return f'{self.razon_social}'

    def toJSON(self):
        item = model_to_dict(self)
        # item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']


class Company(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    nrc = models.CharField(max_length=13, unique=True, null=True, blank=True, verbose_name='NRC')
    nit = models.CharField(max_length=17, unique=True, null=True, blank=True, verbose_name='NIT')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    opening_date = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name='Teléfono fijo')
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name='Celular')
    website = models.CharField(max_length=150, unique=True, null=True, blank=True, verbose_name='Website')
    image = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['opening_date'] = self.opening_date.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Compañía'
        verbose_name_plural = 'Compañías'
        default_permissions = ()
        permissions = {
            ('change_company', 'Can change company')
        }
        ordering = ['id']


class Sale(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    doc_type = models.CharField(max_length=15, null=True, blank=True, verbose_name='Tipo doc.')
    doc_ser = models.CharField(max_length=15, null=True, blank=True, verbose_name='Serie doc.')
    doc_num = models.CharField(max_length=15, null=True, blank=True, verbose_name='Num. doc.')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    nulled = models.BooleanField(default=False, verbose_name='Anulado')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_updated_by',
                                      null=True, blank=True)    
    nulled_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.cli.names

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Sale, self).save()

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['cli'] = self.cli.toJSON()
        item['doc_type'] = self.doc_type
        item['doc_ser'] = self.doc_ser
        item['doc_num'] = self.doc_num
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()] #Esto automáticamente muestra los detalles de una venta
        return item

    def delete(self, using=None, keep_parents=False):
        # for det in self.detsale_set.all():
        for det in self.detsale_set.filter(prod__is_inventoried=True):
            det.prod.stock += det.cant
            det.prod.save()
        super(Sale, self).delete()

    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().aggregate(
            result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['id']


class Entry(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    doc_type = models.CharField(max_length=15, null=True, blank=True, verbose_name='Tipo doc.')
    doc_ser = models.CharField(max_length=15, null=True, blank=True, verbose_name='Serie doc.')
    doc_num = models.CharField(max_length=15, null=True, blank=True, verbose_name='Num. doc.')
    supplier_doc_num = models.CharField(max_length=15, null=True, blank=True, verbose_name='Num. doc. Proveedor')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    nulled = models.BooleanField(default=False, verbose_name='Anulado')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      null=True, blank=True)    
    nulled_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.supplier.razon_social

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Entry, self).save()

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):       
        item = model_to_dict(self)
        item['number'] = self.get_number()
        if not self.supplier == None:
            item['supplier'] = self.supplier.toJSON() #Pasa esto cuando la entrada es nula
        item['doc_type'] = self.doc_type
        item['doc_ser'] = self.doc_ser
        item['doc_num'] = self.doc_num
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detentry_set.all()] #Esto automáticamente muestra los detalles de una venta
        return item

    def delete(self, using=None, keep_parents=False):
        # for det in self.detsale_set.all():
        for det in self.detentry_set.filter(prod__is_inventoried=True):
            det.prod.stock -= det.cant
            det.prod.save()
        super(Entry, self).delete()

    def calculate_invoice(self):
        subtotal = self.entryproduct_set.all().aggregate(
            result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['id']


class DetEntry(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    cost = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['entry'])
        item['prod'] = self.prod.toJSON()
        item['cost'] = f'{self.cost:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Entrada'
        verbose_name_plural = 'Detalle de Entradas'
        default_permissions = ()
        ordering = ['id']




class Movements(BaseModel):
    sale = models.ForeignKey(Sale, null=True, blank=True, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, null=True, blank=True, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    doc_ser = models.CharField(max_length=15, null=True, blank=True, verbose_name='Serie doc.')
    doc_num = models.CharField(max_length=15, null=True, blank=True, verbose_name='Num. doc.')
    type_mov = models.CharField(max_length=1, blank=True, null=True, verbose_name='Tipo Mov.')
    cost = models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2, null=True, blank=True, verbose_name='Costo')
    cant = models.IntegerField(default=0)


    def __str__(self):
        return self.prod.name

    class Meta:
        verbose_name = 'Movimiento de Kardex'
        verbose_name_plural = 'Movimientos de Kardex'
        ordering = ['id']


class TiposDoc(BaseModel):    
    name = models.CharField(max_length=150)
    abrv = models.CharField(max_length=3, unique=True)
    last_number = models.CharField(max_length=15)
    last_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.created_by = user
            else:
                self.updated_by = user
        super(TiposDoc, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = 'Tipo Doc'
        verbose_name_plural = 'Tipos Documentos'
        ordering = ['name']
        

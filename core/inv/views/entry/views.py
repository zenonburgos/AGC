from django.utils import timezone
import json
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View

from core.inv.forms import EntryForm, SupplierForm

from core.inv.mixins import ExistsCompanyMixin, ValidatePermissionRequiredMixin
from core.inv.models import DetEntry, Entry, Movements, Product, Supplier, TiposDoc, Branch

from crum import get_current_request

class EntryListView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, ListView):
    model = Entry
    template_name = 'entry/list.html'
    permission_required = 'view_entry'    
    
    def post(self, request, *args, **kwargs):
        data = {}
        tmov=TiposDoc.objects.get(abrv=self.kwargs['tipomov'])
        try:
            action = request.POST['action']
            if action == 'searchdata':
                
                data = []
                position = 1
                for i in Entry.objects.filter(doc=tmov.id):
                    item = i.toJSON()
                    if i.supplier == None:
                        item['supplier'] = 'no definido'
                    item['position'] = position
                    data.append(item)
                    position += 1
            elif action == 'search_details_prod':
                data = []
                for i in DetEntry.objects.filter(entry_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # Acá se ignora cualquier variable que venga de POST u otra función
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Entradas'
        context['create_url'] = reverse_lazy('inv:entry_create') ##no interfiere en ninguna parte
        context['list_url'] = reverse_lazy('inv:entry_list') ##no interfiere en ninguna parte
        context['entity'] = 'Entradas'
        context['tipomov'] = self.kwargs['tipomov']
        return context


class EntryCreateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entry/create.html'
    success_url = reverse_lazy('inv:entry_list')
    permission_required = 'add_entry'
    url_redirect = success_url
    request = get_current_request()
    
    def post(self, request, *args, **kwargs):
        
        data = {}
        try:
            action = request.POST['action']
            dataDoc = []        
            
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term']
                # products = Product.objects.filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter()
                if len(term):
                    products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))

                itemno = 1
                # for i in products.exclude(id__in=ids_exclude):
                for i in products:
                    item = i.toJSON()  # Este es un método que existe en modelo Product, que convierte sus campos en JSON
                    item['value'] = i.product_type
                    # item['text'] = i.name  # Select2 recibe la data con text
                    item['itemno'] = itemno
                    data.append(item)
                    itemno += 1
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term']
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term).filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))
                itemno = 1
                # for i in products.exclude(id__in=ids_exclude)[0:10]:
                for i in products[0:10]:
                    item = i.toJSON()
                    item['text'] = i.product_type
                    item['itemno'] = itemno
                    data.append(item)
                    itemno += 1
            elif action == 'add':
                with transaction.atomic():
                    sessionbranch = request.session['almacen']
                    alm = Branch.objects.get(id=sessionbranch.id)

                    ents = json.loads(request.POST['ents'])

                    entry = Entry()
                    entry.branch = alm
                    entry.date_joined = ents['date_joined']
                    entry.doc = TiposDoc.objects.get(pk=ents['doc'])
                    entry.doc_ser = ents['doc_ser']
                    entry.doc_num = ents['doc_num']
                    entry.supplier_id = ents['supplier']
                    entry.supplier_doc_num = ents['supplier_doc_num']
                    entry.subtotal = float(ents['subtotal'])
                    entry.iva = float(ents['iva'])
                    entry.total = float(ents['total'])
                    entry.save()

                    for i in ents['products']:
                        # Guardar en Detalle documento
                        det = DetEntry()
                        det.entry_id = entry.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.cost = float(i['cost'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # Guardar en Movimientos
                        mov = Movements()
                        mov.entry_id = entry.id
                        mov.prod_id = i['id']
                        mov.date = ents['date_joined']
                        mov.doc_ser = ents['doc_ser']
                        mov.doc_num = ents['doc_num']
                        mov.type_mov = 'E'
                        mov.cost = float(i['cost'])
                        mov.cant = int(i['cant'])
                        mov.save()
                        # Actualizar control de documentos TiposDoc
                        tdoc = TiposDoc.objects.get(abrv=self.kwargs['tipomov'])
                        tdoc.last_number = ents['doc_num']
                        tdoc.last_date = ents['date_joined']
                        tdoc.save()
                        # Recalcular stock al agregar
                        if det.prod.is_inventoried:
                            det.prod.stock += det.cant
                            # if det.cost > det.prod.cost:
                            det.prod.cost = det.cost
                            det.prod.save()                            
                    data = {'id': entry.id}
            elif action == 'search_suppliers':
                data = []
                term = request.POST['term']
                suppliers = Supplier.objects.filter(Q(razon_social__icontains=term) |
                                                Q(nrc__icontains=term) |
                                                Q(nit__icontains=term))[0:10]
                for i in suppliers:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_supplier':
                with transaction.atomic():
                    frmSupplier = SupplierForm(request.POST)
                    data = frmSupplier.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_num_doc(self):
        # ser = ents['doc_ser']
        for i in TiposDoc.objects.filter(abrv=self.kwargs['tipomov']):
            numDoc = i.last_number
        return numDoc

    # Acá se ignora cualquier variable que venga de POST u otra función
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NUEVA ENTRADA DE MERCADERÍA'
        context['entity'] = 'Entradas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['numdoc'] = self.get_num_doc()
        context['tipomov'] = self.kwargs['tipomov'] #Esto lo extrae del parametro de la url
        context['frmSupplier'] = SupplierForm()
        
        return context


class EntryUpdateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entry/create.html'
    # success_url = reverse_lazy('inv:entry_list')
    permission_required = 'inv.change_entry'
    # url_redirect = success_url
   
    def get_form(self, form_class=None):
        instance = self.get_object()
        form = EntryForm(instance=instance)
        if instance.supplier != None:
            form.fields['supplier'].queryset = Supplier.objects.filter(id=instance.supplier.id)
        return form

    def get_details_product(self):
        data = []
        itemno = 1        
        try:
            for i in DetEntry.objects.filter(entry_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                item['cost'] = i.cost
                item['itemno'] = itemno
                data.append(item)
                itemno = itemno + 1
        except:            
            pass
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        
        try:
            action = request.POST['action']
            
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term']
                # products = Product.objects.filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter()
                if len(term):
                    products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))

                itemno = 1
                # for i in products.exclude(id__in=ids_exclude):
                for i in products.exclude:
                    item = i.toJSON()  # Este es un método que existe en modelo Product, que convierte sus campos en JSON
                    item['value'] = i.name
                    # item['text'] = i.name  # Select2 recibe la data con text
                    item['itemno'] = itemno
                    data.append(item)
                    itemno += 1
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term']
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term).filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))
                itemno = 1
                # for i in products.exclude(id__in=ids_exclude)[0:10]:
                for i in products[0:10]:
                    item = i.toJSON()
                    item['text'] = i.product_type
                    item['itemno'] = itemno
                    data.append(item)
                    itemno += 1
            elif action == 'edit':
                with transaction.atomic():
                    ents = json.loads(request.POST['ents'])
                    # sale = Sale.objects.get(pk=self.get_object().id) #Forma 1
                    entry = self.get_object()
                    entry.date_joined = ents['date_joined']
                    # entry.doc_type = ents['doc_type']
                    entry.doc = TiposDoc.objects.get(pk=ents['doc'])
                    entry.doc_ser = ents['doc_ser']
                    entry.doc_num = ents['doc_num']
                    entry.cli_id = ents['supplier']
                    entry.subtotal = float(ents['subtotal'])
                    entry.iva = float(ents['iva'])
                    entry.total = float(ents['total'])
                    entry.save()
                    entry.detentry_set.all().delete()
                    entry.movements_set.all().delete()

                    for i in ents['products']:
                        # Guardar en Detalle documento
                        det = DetEntry()
                        det.entry_id = entry.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.cost = float(i['cost'])                        
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.prod.save()
                        # Guardar en Movimientos
                        mov = Movements()
                        mov.entry_id = entry.id
                        mov.prod_id = i['id']
                        mov.date = ents['date_joined']
                        mov.doc_num = ents['doc_num']
                        mov.type_mov = 'E'                        
                        mov.cant = int(i['cant'])
                        mov.save()
                        
                        # Recalcular stock
                        # det.prod.stock -= det.cant
                        # det.prod.save()
                    data = {'id': entry.id}
            elif action == 'search_suppliers':
                data = []
                term = request.POST['term']
                suppliers = Supplier.objects.filter(Q(razon_social__icontains=term) |
                                                Q(nrc__icontains=term) |
                                                Q(nit__icontains=term))[0:10]
                for i in suppliers:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_supplier':
                with transaction.atomic():
                    frmSupplier = SupplierForm(request.POST)
                    data = frmSupplier.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return JsonResponse(data, safe=False)

    # Acá se ignora cualquier variable que venga de POST u otra función
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Entrada'
        context['entity'] = 'Entradas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(), cls=DjangoJSONEncoder)
        context['frmClient'] = SupplierForm()
        context['tipomov'] = self.kwargs['tipomov'] #Esto lo extrae del parametro de la url
        return context


class EntryDeleteView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Entry
    template_name = 'entry/delete.html'
    success_url = reverse_lazy('inv:entry_list')
    permission_required = 'delete_entry'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    # Acá se ignora cualquier variable que venga de POST u otra función
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Entrada'
        context['entity'] = 'Entradas'
        context['list_url'] = self.success_url
        return context


def EntryCancel(request, id):
    entry = Entry.objects.filter(pk=id).first()
    context = {}
    template_name = 'entry/anular.html'
    now = timezone.now()

    if not entry:
        return redirect('inv:entry_list')

    if request.method=='GET':        
        contexto = {
            'obj': entry,
            'tipomov': request['tipomov'], #Esto lo extrae del parametro de la url
            'list_url': reverse_lazy('inv:entry_list'),
        }

    if request.method=='POST':
        for det in DetEntry.objects.filter(entry=id):
            det.prod.stock += det.cant
            det.cant = 0            
            det.save()
            det.prod.save()
        
        entry.nulled = True
        entry.subtotal = 0
        entry.total = 0
        entry.nulled_at = now
        entry.save()
        return redirect('inv:entry_list')
    
    return render(request, template_name, contexto)
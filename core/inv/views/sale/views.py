import json
from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from weasyprint import HTML, CSS

from core.inv.forms import SaleForm, ClientForm
from core.inv.mixins import ValidatePermissionRequiredMixin, ExistsCompanyMixin
from core.inv.models import Sale, Product, DetSale, Movements, Client

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders


class SaleListView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Sale.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('inv:sale_create')
        context['list_url'] = reverse_lazy('inv:sale_list')
        context['entity'] = 'Ventas'
        return context


class SaleCreateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('inv:sale_list')
    permission_required = 'add_sale'
    url_redirect = success_url

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
                for i in products.exclude(id__in=ids_exclude):
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
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.product_type
                    item['itemno'] = itemno
                    data.append(item)
                    itemno += 1
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])

                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.doc_type = vents['doc_type']
                    sale.doc_ser = vents['doc_ser']
                    sale.doc_num = vents['doc_num']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()

                    for i in vents['products']:
                        # Guardar en Detalle documento
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['price'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # Guardar en Movimientos
                        mov = Movements()
                        mov.sale_id = sale.id
                        mov.prod_id = i['id']
                        mov.date = vents['date_joined']
                        mov.doc_ser = vents['doc_ser']
                        mov.doc_num = vents['doc_num']
                        mov.type_mov = 'S'
                        mov.cant = int(i['cant'])
                        mov.save()
                        # Recalcular stock
                        if det.prod.is_inventoried:
                            det.prod.stock -= det.cant
                            det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(Q(names__icontains=term) |
                                                Q(surnames__icontains=term) |
                                                Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmClient'] = ClientForm()
        return context


class SaleUpdateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('inv:sale_list')
    permission_required = 'inv.change_sale'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SaleForm(instance=instance)
        form.fields['cli'].queryset = Client.objects.filter(id=instance.cli.id)
        return form

    def get_details_product(self):
        data = []
        itemno = 1
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                item['price'] = i.price
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
                for i in products.exclude(id__in=ids_exclude):
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
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    item['itemno'] = itemno
                    data.append(item)
                    itemno += 1
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id) #Forma 1
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    sale.doc_type = vents['doc_type']
                    sale.doc_ser = vents['doc_ser']
                    sale.doc_num = vents['doc_num']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    sale.detsale_set.all().delete()
                    sale.movements_set.all().delete()
                    for i in vents['products']:
                        # Guardar en Detalle documento
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['price'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # Guardar en Movimientos
                        mov = Movements()
                        mov.sale_id = sale.id
                        mov.prod_id = i['id']
                        mov.date = vents['date_joined']
                        mov.doc_num = vents['doc_num']
                        mov.type_mov = 'S'
                        mov.cant = int(i['cant'])
                        mov.save()
                        # Recalcular stock
                        # det.prod.stock -= det.cant
                        # det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(Q(name__icontains=term) |
                                                Q(surname__icontains=term) |
                                                Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(), cls=DjangoJSONEncoder)
        context['frmClient'] = ClientForm()
        return context


class SaleDeleteView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('inv:sale_list')
    permission_required = 'delete_sale'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context


class SaleInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/invoice.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('inv:sale_list'))

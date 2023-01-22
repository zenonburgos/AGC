from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.inv.forms import ProductForm, BrandForm, CategoryForm
from core.inv.mixins import ValidatePermissionRequiredMixin
from core.inv.models import Brand, Group, Product, Category, Branch


class ProductListView(ValidatePermissionRequiredMixin, ListView):
    model = Product
    template_name = 'product/list.html'
    permission_required = 'view_product'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Product.objects.all():
                    item = i.toJSON()
                    if item['name'] is not None:
                        item['name'] = i.name.title()
                    data.append(item)
                # print (item['product_type'])
            else:
                data['error'] = 'Ha ocurrido un error con el listado de productos.'
        except Exception as e:            
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('inv:product_create')
        context['list_url'] = reverse_lazy('inv:product_list')
        context['entity'] = 'Productos'        
        return context


class ProductCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('inv:product_list')
    permission_required = 'add_product'
    url_redirect = success_url
    context_object_name = 'obj'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            elif action == 'search_brands':
                data = []                
                term = request.POST['term']
                # data.append({'id': term, 'text': term})
                brands = Brand.objects.filter(name__icontains=term)
                for i in brands[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'search_cats':
                data = []                
                term = request.POST['term']
                # data.append({'id': term, 'text': term})
                brands = Category.objects.filter(name__icontains=term)
                for i in brands[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'create_brand':
                with transaction.atomic():
                    frmBrand = BrandForm(request.POST)
                    data = frmBrand.save()
            elif action == 'create_cat':
                with transaction.atomic():
                    frmCategory = CategoryForm(request.POST)
                    data = frmCategory.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('inv:product_list')
        context['action'] = 'add'
        context["categories"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        context["groups"] = Group.objects.all()
        context['frmBrand'] = BrandForm()
        context['frmCategory'] = CategoryForm()        
        return context


class ProductUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('inv:product_list')
    permission_required = 'change_product'
    url_redirect = success_url
    context_object_name = 'obj'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('inv:product_list')
        context['action'] = 'edit'
        context["categories"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        context["groups"] = Group.objects.all()
        return context


class ProductDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('inv:product_list')
    permission_required = 'delete_product'
    url_redirect = success_url

    @method_decorator(login_required)
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
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('inv:product_list')
        return context

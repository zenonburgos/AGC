from django.urls import path

from core.inv.views.category.views import *
from core.inv.views.client.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView
from core.inv.views.company.views import CompanyUpdateView
from core.inv.views.dashboard.views import DashboardView
from core.inv.views.entry.views import EntryCancel, EntryCreateView, EntryDeleteView, EntryListView, EntryUpdateView
from core.inv.views.product.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
from core.inv.views.sale.views import SaleCreateView, SaleListView, SaleUpdateView, SaleDeleteView, SaleInvoicePdfView
from core.inv.views.supplier.views import SupplierCreateView, SupplierDeleteView, SupplierListView, SupplierUpdateView
from core.inv.views.tests.views import TestView

app_name = 'inv'

urlpatterns = [
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/form/', CategoryFormView.as_view(), name='category_form'),
    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # supplier
    path('supplier/list/', SupplierListView.as_view(), name='supplier_list'),
    path('supplier/add/', SupplierCreateView.as_view(), name='supplier_create'),
    path('supplier/update/<int:pk>/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier/delete/<int:pk>/', SupplierDeleteView.as_view(), name='supplier_delete'),
    # Test
    path('test/', TestView.as_view(), name='test'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # entry
    path('entry/list/<str:tipomov>/', EntryListView.as_view(), name='entry_list'),
    path('entry/add/<str:tipomov>/', EntryCreateView.as_view(), name='entry_create'),    
    path('entry/update/<int:pk>/<str:tipomov>/', EntryUpdateView.as_view(), name='entry_update'),
    path('entry/delete/<int:pk>/', EntryDeleteView.as_view(), name='entry_delete'),
    path('entry/cancel/<int:id>/<str:tipomov>/', EntryCancel, name='entry_cancel'), ## Para ingresar como anulado

    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
]

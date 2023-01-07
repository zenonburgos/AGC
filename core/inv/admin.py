from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin

from core.inv.models import Brand, Category, Group, Entry, Product, Sale, Supplier, \
    Movements, TiposDoc, ProductImage

from core.accounts.models import Account

# @admin.register(Account)
# class AccountAdmin(UserAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
#     list_display_links = ('email', 'first_name', 'last_name')
#     readonly_fields = ('last_login', 'date_joined')
#     ordering = ('-date_joined',)

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

@admin.register(Category)
class CategoryProduct(ImportExportModelAdmin):
    # pass
    fields = ('name', 'slug', 'image', 'parent')
    list_display = ('name', 'slug', 'parent')

# admin.site.register(Category)


@admin.register(Brand)
class BrandProduct(ImportExportModelAdmin):
    fields = ('name', 'slug', 'image')
    list_display = ('name', 'slug')


@admin.register(Group)
class GroupProduct(ImportExportModelAdmin):
    fields = ('category', 'name', 'slug', 'image')
    list_display_links = ('name',)
    list_display = ('name', 'slug', 'category')
    list_editable = ('category',)


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    fields = ('code', 'barcode', 'name', 'description', 'slug', 'product_type', 'category', 'model', 'brand', 'cost', 'fact', 'fact2', 'fact3', 'price', 'price2', 'price3', 'image', 'is_inventoried', 'active', 'store', 'special_offers', 'featured_products', 'best_seller', 'is_hot')
    list_display_links = ('name', 'model')
    list_display = ('name', 'model', 'marca', 'store', 'brand', 'category', 'active', 'catalogue', 'special_offers', 'featured_products', 'best_seller', 'is_hot', 'created_at')
    list_editable = ('active', 'catalogue', 'brand', 'category', 'store', 'special_offers', 'featured_products', 'best_seller', 'is_hot')
    search_fields = ['code', 'name']
    list_per_page = 15
    inlines = [
        ProductImageAdmin
    ]
    

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    fields = ('nrc', 'razon_social', 'nit', 'address', 'active')
    list_display = ('nrc', 'nit')
    

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    fields = ('supplier', 'date_joined', 'doc_type', 'doc_ser', 'doc_num', 'subtotal', 'iva', 'total_iva', 'total')
    list_display = ('supplier', 'date_joined', 'doc_type', 'doc_ser', 'doc_num', 'subtotal', 'total')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    fields = ('cli', 'date_joined', 'doc_type', 'doc_ser', 'doc_num', 'subtotal', 'iva', 'total_iva', 'total')
    list_display = ('cli', 'date_joined', 'doc_type', 'doc_ser', 'doc_num', 'subtotal', 'total')


@admin.register(Movements)
class MovsAdmin(admin.ModelAdmin):
    fields = ('date', 'doc_ser', 'doc_num', 'type_mov', 'cost', 'cant')
    list_display = ('date', 'doc_ser', 'doc_num', 'type_mov', 'cost', 'cant')

# admin.site.register(Product)

@admin.register(TiposDoc)
class TiposDocAdmin(admin.ModelAdmin):
    fields = ('name', 'abrv', 'last_number', 'last_date')
    list_display = ('name', 'abrv', 'last_number', 'last_date')
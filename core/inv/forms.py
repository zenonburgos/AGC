from datetime import datetime

from django.forms import *
from django import forms

from core.inv.models import Category, Entry, Product, Client, Sale, Company, Supplier, Brand


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['name'].required = False
        # self.fields['slug'].required = False

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre para la nueva Categoría',
                },
            ),
            'slug': TextInput(
                attrs={
                    'placeholder': 'Especifique slug, reemplace espacios por guiones y todo en minúscula, no use caracteres especiales.',
                }
            )
        }
        exclude = ['created_by', 'updated_by', 'is_active', 'slug']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class BrandForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['name'].required = False
        # self.fields['slug'].required = False

    class Meta:
        model = Brand
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre para la nueva Marca',
                },
            ),
            'slug': TextInput(
                attrs={
                    'placeholder': 'Especifique slug, reemplace espacios por guiones y todo en minúscula, no use caracteres especiales.',
                }
            )
        }
        exclude = ['created_by', 'updated_by', 'is_active', 'slug']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['brand'].queryset = Brand.objects.none() 
        # self.fields['category'].queryset = Category.objects.none() 
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['code'].widget.attrs['autofocus'] = True
        self.fields['description'].widget.attrs['rows'] = 3
        # self.fields['stock'].widget.attrs['readonly'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'cost': TextInput(
                attrs={
                    
                }
            ),
            'fact': TextInput(
                attrs={
                    
                }
            ),
            'price': TextInput(
                attrs={
                    
                }
            ),
            'fact2': TextInput(
                attrs={
                    
                }
            ),
            'fact3': TextInput(
                attrs={
                    
                }
            ),
            'price2': TextInput(
                attrs={
                    
                }
            ),
            'price3': TextInput(
                attrs={
                    
                }
            ),
            'stock': TextInput(
                attrs={
                    
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'placeholder js-states form-control'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'placeholder js-states form-control'
    }))

    search = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'placeholder js-states form-control'
    }))


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'date_of_birth': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control flatpickr-input active',
                    'id': 'datejoined',
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }
        exclude = ['updated_by', 'created_by', 'active']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class SupplierForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nrc'].widget.attrs['autofocus'] = True

    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {            
            'nit': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nit',
                }
            ),            
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),            
        }
        exclude = ['updated_by', 'created_by', 'active']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Client.objects.none()
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                # 'class': 'placeholder js-states form-control',
                'class': 'custom-select select2',
                'autofocus': True,
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control flatpickr-input active',
                    'aria-label': 'Small',
                    'aria-describedby': 'inputGroup-sizing-sm',
                    'id': 'date',
                    # 'data-target': '#date_joined',
                    # 'data-toggle': 'datetimepicker'
                }
            ),
            'doc_ser': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'aria-label': 'Small',
                'aria-describedby': 'inputGroup-sizing-sm',
            }),
            'doc_num': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'aria-label': 'Small',
                'aria-describedby': 'inputGroup-sizing-sm',
            }),
            'iva': TextInput(attrs={
                'class': 'form-control'
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control'
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control'
            })
        }
        exclude = ['updated_by', 'created_by', 'active']


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['name'].required = False
        # self.fields['slug'].required = False

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre para la nueva Categoría',
                },
            ),
            'nrc': TextInput(
                attrs={
                    'placeholder': 'Ingrese Número de Registro de Contribuyente (NRC)',
                },
            ),
            'nit': TextInput(
                attrs={
                    'placeholder': 'Ingrese Número Número de Identificación Tributaria (NIT)',
                },
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese dirección registrada',
                },
            ),
            'opening_date': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control flatpickr-input active',
                    'id': 'datejoined',
                }
            ),
            'mobile': TextInput(
                attrs={
                    'placeholder': 'Ingrese número de teléfono móvil',
                },
            ),
            'phone': TextInput(
                attrs={
                    'placeholder': 'Ingrese número de teléfono fijo',
                },
            ),
            'website': TextInput(
                attrs={
                    'placeholder': 'Website (opcional)',
                },
            ),
        }
        exclude = ['created_by', 'updated_by', 'is_active', 'slug']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.none()

    class Meta:
        model = Entry
        fields = '__all__'
        widgets = {
            'supplier': Select(attrs={
                # 'class': 'placeholder js-states form-control',
                'class': 'custom-select select2',
                'autofocus': True,
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control flatpickr-input active',
                    'aria-label': 'Small',
                    'aria-describedby': 'inputGroup-sizing-sm',
                    'id': 'date',
                    # 'data-target': '#date_joined',
                    # 'data-toggle': 'datetimepicker'
                }
            ),
            'doc_ser': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'aria-label': 'Small',
                'aria-describedby': 'inputGroup-sizing-sm',
            }),
            'doc_num': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'aria-label': 'Small',
                'aria-describedby': 'inputGroup-sizing-sm',
            }),
            'iva': TextInput(attrs={
                'class': 'form-control'
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control'
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control'
            })
        }
        exclude = ['updated_by', 'created_by', 'active']
from crum import get_current_request
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from core.inv.models import Company


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('inv:dashboard')
        return self.url_redirect

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request = get_current_request()
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        if 'group' in request.session:
            group = request.session['group']
            perms = self.get_perms()
            for p in perms:
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'No tiene permiso para ingresar a este módulo')
                    return HttpResponseRedirect(self.get_url_redirect())
            return super().get(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())


class ExistsCompanyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if Company.objects.all().exists():
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No se puede facturar si no está registrada la compañía.')
        return redirect('inv:dashboard')


# class ValidatePermissionRequiredMixin(object):
#     permission_required = ''
#     url_redirect = None
#
#     def get_perms(self):
#         if isinstance(self.permission_required, str):
#             perms = (self.permission_required,)
#         else:
#             perms = self.permission_required
#         return perms
#
#     def get_url_redirect(self):
#         if self.url_redirect is None:
#             return reverse_lazy('login')
#         return self.url_redirect
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.has_perms(self.get_perms()):
#             return super().dispatch(request, *args, **kwargs)
#         messages.error(request, 'No tiene permiso para ingresar a este módulo.')
#         return HttpResponseRedirect(self.get_url_redirect())

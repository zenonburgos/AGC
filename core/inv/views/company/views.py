from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.inv.forms import CompanyForm
from core.inv.mixins import ValidatePermissionRequiredMixin
from core.inv.models import Company


class CompanyUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('inv:dashboard')
    permission_required = 'change_company'
    url_redirect = success_url

    def get_object(self, queryset=None):
        company = Company.objects.all()
        if company.exists():
            return company[0]
        return Company()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                instance = self.get_object()
                if instance.pk is not None:
                    form = CompanyForm(request.POST, request.FILES, instance=instance)
                    data = form.save()
                else:
                    form = CompanyForm(request.POST, request.FILES)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('inv:category_list')
        context['action'] = 'edit'
        return context
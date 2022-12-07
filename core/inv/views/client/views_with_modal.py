from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.inv.forms import ClientForm
from core.inv.models import Client


class ClientView(TemplateView):
    template_name = 'client/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Client.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                cli = Client()
                cli.name = request.POST['name']
                cli.surname = request.POST['surname']
                cli.dni = request.POST['dni']
                cli.date_of_birth = request.POST['date_of_birth']
                cli.address = request.POST['address']
                cli.gender = request.POST['gender']
                cli.save()
            elif action == 'edit':
                cli = Client.objects.get(pk=request.POST['id'])
                cli.name = request.POST['name']
                cli.surname = request.POST['surname']
                cli.dni = request.POST['dni']
                cli.date_of_birth = request.POST['date_of_birth']
                cli.address = request.POST['address']
                cli.gender = request.POST['gender']
                cli.active = request.POST['active']
                cli.save()
            elif action == 'delete':
                cli = Client.objects.get(pk=request.POST['id'])
                # cli.delete()
                cli.active = False
                cli.save()
            elif action == 'activar':
                cli = Client.objects.get(pk=request.POST['id'])
                # cli.delete()
                cli.active = True
                cli.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('inv:client')
        context['entity'] = 'Clientes'
        context['form'] = ClientForm()
        return context



from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from core.user.models import User
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Comercial Perdomo. Por favor, active su cuenta.'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Gracias por registrarse con nosotros. Hemos enviado un email de verificación a su bandeja de entrada.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user:
            auth.login(request, user)
            messages.success(request, 'Has ingresado correctamente.')
            # return redirect('cus_dashboard')
            return redirect('index')
        else:
            messages.error(request, 'Credenciales inválidas.')
            return redirect('cus_login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'cus_login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Has salido del sitio web.')
    return redirect('cus_login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Felicidades. Su cuenta está activa. A continuación intente acceder con sus credenciales')
        return redirect('cus_login')
    else:
        messages.error(request, 'Enlace de activación inválido.')
        return redirect('cus_register')

@login_required(login_url = 'cus_login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
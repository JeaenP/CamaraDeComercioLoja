from django.shortcuts import render
from django.views import View
import json 
from django.http import JsonResponse
from django.contrib.auth.models import User 
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.shortcuts import redirect
from django.contrib import auth

# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'El correo es invalido'}, status = 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'El correo electronico ya esta en uso'}, status = 409)
        return JsonResponse({'email_valid': True})
    
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'El usuario solo debe contener numeros y letras'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Usuario en uso, eleja otro '}, status=409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render (request, 'authentication/register.html')
    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = { 
            'fieldValues': request.POST
        }
        if not User.objects.filter(username = username).exists():
            if not User.objects.filter(email = email).exists():
                if len(password) < 6:
                    messages.error(request, 'La contraseña es demasiado corta!')  
                    return render (request, 'authentication/register.html', context)

                user = User.objects.create_user(username = username, email = email, )
                user.set_password(password)
                user.is_active = False;
                user.save()
                email_subject = 'Activar cuenta Càmara de Comercio'

                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'http://'+domain+link
                email_body = 'Hi ' + user.username + 'Por favor use este link para verificar su cuenta ' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Cuenta creada correctamente!')  
        return render (request, 'authentication/register.html')
    
class VerificationView(View):
    def get(self, request, uidb64, token): 
        

        try: 
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message=' + 'El usuario ya esta activado')
            if user.is_active: 
                return redirect('login')
            user.is_active = True
            user.save() 

            messages.success(request, 'La cuenta ha sido activada exitosamente')
            return redirect('login')
        except Exception as ex:
            pass

        return redirect('login')
      
    
    
    
class LoginView(View):
    def get(self, request): 
        return render(request, 'authentication/login.html')
    
    def post(self, request): 
        username = request.POST['username']
        password = request.POST['password']

        if username and password: 
            user = auth.authenticate(username = username, password = password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    
                    return redirect ('home')
                messages.error(request, 'El usuario no ha sido activado, por favor revisar su correo.')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Usuario/Contraseña incorrecto.')


            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Complete toda la información primero.')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Sesiòn cerrada exitosamente')
        return redirect('login')
    

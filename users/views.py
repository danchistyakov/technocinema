from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .forms import RegisterForm, CustomAuthenticationForm
from django.contrib.messages.api import get_messages
import logging


def send_activation_email(request, user):
    try:
        current_site = get_current_site(request)
        subject = 'Активируйте ваш аккаунт TechnoCinema'
        message = render_to_string('users/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        email = EmailMessage(subject, message, '4i.danila@gmail.com', [user.email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        return True
    except Exception as e:
        logging.exception(e)
        return False


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            if send_activation_email(request, user):
                messages.success(
                    request, f'Пожалуйста, проверьте вашу почту ({user.email}) для активации аккаунта.')
                return redirect('login')
            else:
                messages.error(request, 'Не удалось отправить письмо активации. Попробуйте ещё раз.')
                user.delete()
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле {field}")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш аккаунт успешно активирован. Теперь вы можете войти.')
    else:
        print('error')
        messages.error(request, 'Ссылка для активации недействительна.')
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    storage = get_messages(request)
    for _ in storage:
        pass
    logout(request)

    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')

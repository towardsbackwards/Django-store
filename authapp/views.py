from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse
from authapp.models import ShopUser
from django.conf import settings
from django.core.mail import send_mail

def login(request):
    if request.method == 'POST':
        # 1. получить данные которые нам отправили
        print('POST', request.POST)
        print('GET', request.GET)
        # form = ShopUserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password) # вот она, проверка на наличие пользователя
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
        else:
            print('Зашли???')
            form = ShopUserLoginForm(data=request.POST)
            return render(request, 'login.html', {'login_form': form, 'error': True})
    else:
        form = ShopUserLoginForm()
        return render(request, 'login.html', {'login_form': form})

def register(request):
    title = 'Registration'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('На вашу почту отправлено сообщение для подтверждения учетной записи')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('Сообщение для подтверждения регистрации не удалось отправить')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
        content = {'title': title, 'register_form': register_form}

        return render(request, 'register.html', content)



def edit(request):
    return HttpResponseRedirect(reverse('main:index'))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index')) # при выходе переход на главную страницу

@transaction.atomic
def edit(request):
    title = 'Edit profile'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            print()
            print("Функция вьюхи отработала сохранение пользователя и его профиля...")
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}
    return render(request, 'edit.html', content)

def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME}, перейдите ' \
        f'по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            print(f'user {user} is activated')
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'verification.html')

    except Exception as e:
        print(f'error activation user : {e.args}')

    return HttpResponseRedirect(reverse('main:index'))
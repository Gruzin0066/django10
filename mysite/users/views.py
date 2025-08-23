from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import CreateView, UpdateView

from mysite import settings
from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, UserPasswordChangeForm
from users.models import User
from users.utils import email_confirmation_token, activation_token_generator


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {'title': 'Авторизация'}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')  # Или на главную
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')  # Или на главную
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    #От ИИ
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Пользователь неактивен до подтверждения email
        user.token_created_at = timezone.now()  # Важно сохранить дату!
        user.verification_token = activation_token_generator.make_token(user)
        user.save()

        # Генерация токена и UID
        token = activation_token_generator.make_token(user)
        print(f"[REGISTER] Generated token: {token}")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print(token, uid, user.pk)

        # Создание ссылки активации
        activation_url = self.request.build_absolute_uri(reverse('activate-account', kwargs={'uidb64': uid, 'token': token}))
        activation_url = mark_safe(activation_url)
        print(activation_url)

        # Отправка письма

        mail_subject = 'Активация вашего аккаунта'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
            'activation_url': activation_url,
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.encoding = 'utf-8'  # Явно указываем кодировку

        # Добавляем заголовки для правильного отображения
        email.extra_headers = {
            'Content-Type': 'text/html; charset="utf-8"',
            'Content-Transfer-Encoding': '8bit',
        }
        email.send()

        messages.success(self.request,
                         'Пожалуйста, подтвердите ваш email для завершения регистрации. Письмо отправлено на указанный адрес.')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/profile.html'
    form_class = UserUpdateForm
    extra_context = {
        'title': 'Личный кабинет',
        'default_image_url': settings.DEFAULT_USER_IMAGE
    }

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, '✅ Ваш профиль успешно сохранён!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '❌ Ошибка сохранения профиля.')
        return super().form_invalid(form)



# От ИИ
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(f"[DEBUG] User: {user.username}, Active: {user.is_active}")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None:
        messages.error(request, 'Пользователь не найден!')
        return redirect('register')

    if user.is_active:
        messages.error(request, 'Аккаунт уже активирован!')
        return redirect('login')

    if user and activation_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Аккаунт успешно активирован! Теперь вы можете войти.')
        return redirect('login')
        # return render(request, 'users/activation_access.html')
    else:
        print(activation_token_generator.check_token(user, token))
        print(f"[DEBUG] Token check failed. User PK: {user.pk}, Token: {token}")
        messages.error(request, 'Недействительная ссылка активации!')
        return redirect('register')
        # return render(request, 'users/activation_error.html')



class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'users/password_change_form.html'


class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
            print(f"Decoded UID: {uid}, User: {user}, Token: {token}")  # Отладка
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print(f"Error decoding UID: {e}")  # Отладка
            user = None

        if user and email_confirmation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Аккаунт успешно активирован! Теперь вы можете войти.')
            return redirect('login')  # Замени на нужный URL
        else:
            print(f"Token check failed: user={user}, token_valid={email_confirmation_token.check_token(user, token) if user else False}")  # Отладка
            messages.error(request, 'Недействительная ссылка активации!')
            return redirect('register')
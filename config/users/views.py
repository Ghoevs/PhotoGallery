from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    CustomUserCreationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm,
    ProfileUpdateForm
)
from .models import User
from .services import send_welcome_email, send_password_change_email


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_welcome_email(user)
        messages.success(self.request, 'Регистрация прошла успешно! Проверьте почту.')
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный email или пароль')
        return super().form_invalid(form)


class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль обновлен!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = 'dogs:index'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы вышли из аккаунта')
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        send_password_change_email(self.request.user)
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:login')
    email_template_name = 'users/password_reset_email.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    ordering = ['-date_joined']
    paginate_by = 10


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'user_id'

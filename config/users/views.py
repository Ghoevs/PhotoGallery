from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from django.contrib import messages
from django.views import View
from django.views.generic import (
    CreateView, TemplateView, ListView, DetailView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    CustomUserCreationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm,
    ProfileUpdateForm
)
from .models import User, Subscription
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


class PrivacyPolicyView(TemplateView):
    template_name = 'users/privacy_policy.html'


class SubscriptionPlansView(TemplateView):
    template_name = 'users/subscription_plans.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_subscription'] = self.request.user.has_subscription
        return context


class SubscriptionCheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'users/subscription_checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan'] = self.kwargs.get('plan', 'month')
        plans = {
            'month': {'name': 'На месяц', 'price': 299},
            'year': {'name': 'На год', 'price': 1990},
            'forever': {'name': 'Навсегда', 'price': 4990},
        }
        context['plan_info'] = plans.get(self.kwargs.get('plan'), plans['month'])
        return context


class SubscriptionSuccessView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        plan = self.kwargs.get('plan', 'month')
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        subscription.activate(plan)
        messages.success(request, 'Подписка успешно активирована!')
        return redirect('users:subscription_success_page')

    def get(self, request, *args, **kwargs):
        return redirect('users:subscription_plans')


class SubscriptionSuccessPageView(LoginRequiredMixin, TemplateView):
    template_name = 'users/subscription_success.html'
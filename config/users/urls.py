from django.urls import path
from . import views
from .forms import CustomAuthenticationForm

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('all/', views.UserListView.as_view(), name='user_list'),
    path('subscription/', views.SubscriptionPlansView.as_view(), name='subscription_plans'),
    path('subscription/checkout/<str:plan>/', views.SubscriptionCheckoutView.as_view(), name='subscription_checkout'),
    path('subscription/success/<str:plan>/', views.SubscriptionSuccessView.as_view(), name='subscription_success'),
    path('subscription/success/', views.SubscriptionSuccessPageView.as_view(), name='subscription_success_page'),
    path('<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
]
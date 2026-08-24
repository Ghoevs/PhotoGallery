from django.urls import path
from . import views
from . import api_views
from .forms import CustomAuthenticationForm
from rest_framework.authtoken.views import obtain_auth_token

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
    path('all/', views.UserListView.as_view(), name='user_list'),
    path('<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('api/users/', api_views.UserListCreateView.as_view(), name='api_users'),
    path('api/users/me/', api_views.UserDetailView.as_view(), name='api_user_detail'),
    path('api/token/', obtain_auth_token, name='api_token'),
]

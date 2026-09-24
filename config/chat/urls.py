from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='chat_list'),
    path('start/<int:photo_id>/', views.StartChatView.as_view(), name='start_chat'),
    path('<int:chat_id>/', views.ChatDetailView.as_view(), name='chat_detail'),
    path('<int:chat_id>/send/', views.SendMessageView.as_view(), name='send_message'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
]
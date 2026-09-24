from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from dogs.models import Photo
from .models import Chat, Message


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'chat/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        ).order_by('-created_at')


class StartChatView(LoginRequiredMixin, View):
    def get(self, request, photo_id):
        photo = get_object_or_404(Photo, id=photo_id)
        if photo.owner == request.user:
            messages.error(request, 'Вы не можете начать чат с самим собой')
            return redirect('dogs:photo_detail', photo_id=photo.id)

        chat, created = Chat.objects.get_or_create(
            photo=photo,
            buyer=request.user,
            defaults={'seller': photo.owner}
        )
        return redirect('chat:chat_detail', chat_id=chat.id)


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chat/chat_detail.html'
    context_object_name = 'chat'
    pk_url_kwarg = 'chat_id'

    def get_object(self):
        chat = get_object_or_404(Chat, id=self.kwargs['chat_id'])
        if chat.buyer != self.request.user and chat.seller != self.request.user:
            messages.error(self.request, 'У вас нет доступа к этому чату')
            return redirect('chat:chat_list')
        return chat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.object
        chat.messages.filter(is_read=False).exclude(sender=self.request.user).update(is_read=True)
        context['chat_messages'] = chat.messages.all()
        context['other_user'] = chat.seller if chat.buyer == self.request.user else chat.buyer
        return context


class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        if chat.buyer != request.user and chat.seller != request.user:
            messages.error(request, 'У вас нет доступа к этому чату')
            return redirect('chat:chat_list')

        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(chat=chat, sender=request.user, text=text)
        return redirect('chat:chat_detail', chat_id=chat.id)


class NotificationsView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat/notifications.html'
    context_object_name = 'messages_list'

    def get_queryset(self):
        return Message.objects.filter(
            Q(chat__buyer=self.request.user) | Q(chat__seller=self.request.user),
            is_read=False
        ).exclude(sender=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_total'] = self.get_queryset().count()
        return context
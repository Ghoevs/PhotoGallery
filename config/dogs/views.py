from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from .models import Category, Photo, Review
from .forms import PhotoForm, ReviewForm
from .services import send_views_notification
from users.services import send_photo_created_email
from users.models import User


class IndexView(TemplateView):
    template_name = 'dogs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Фотогалерея'
        return context


class PhotoListView(ListView):
    model = Photo
    template_name = 'dogs/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'dogs/photo_detail.html'
    context_object_name = 'photo'
    pk_url_kwarg = 'photo_id'

    def get_object(self, queryset=None):
        photo = super().get_object(queryset)
        if self.request.user != photo.owner:
            photo.views += 1
            photo.save()
            send_views_notification(photo)
        return photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['review_form'] = ReviewForm()
        if self.request.user.is_authenticated:
            context['user_review_count'] = Review.objects.filter(
                user=self.request.user, photo=self.object
            ).count()
        else:
            context['user_review_count'] = 0
        return context


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'dogs/photo_form.html'
    success_url = reverse_lazy('dogs:photo_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Добавить'
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        send_photo_created_email(self.request.user, self.object)
        messages.success(self.request, 'Фотография добавлена!')
        return response


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'dogs/photo_form.html'
    pk_url_kwarg = 'photo_id'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.owner

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете редактировать только свои фотографии')
        return redirect('dogs:photo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Изменить'
        return context

    def get_success_url(self):
        return reverse_lazy('dogs:photo_detail', kwargs={'photo_id': self.object.id})


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = 'dogs/photo_confirm_delete.html'
    pk_url_kwarg = 'photo_id'
    success_url = reverse_lazy('dogs:photo_list')

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.owner

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете удалять только свои фотографии')
        return redirect('dogs:photo_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Фотография удалена!')
        return super().delete(request, *args, **kwargs)


class UserPhotoListView(ListView):
    model = Photo
    template_name = 'dogs/user_photos.html'
    context_object_name = 'photos'
    paginate_by = 6

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, id=self.kwargs['user_id'])
        queryset = Photo.objects.filter(owner=self.profile_user)
        if not self.request.user.is_staff and self.request.user != self.profile_user:
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'dogs/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'dogs/review_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['photo'] = get_object_or_404(Photo, id=self.kwargs['photo_id'])
        return kwargs

    def form_valid(self, form):
        photo = get_object_or_404(Photo, id=self.kwargs['photo_id'])
        form.instance.photo = photo
        form.instance.user = self.request.user
        messages.success(self.request, 'Отзыв добавлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dogs:photo_detail', kwargs={'photo_id': self.kwargs['photo_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo'] = get_object_or_404(Photo, id=self.kwargs['photo_id'])
        return context


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'dogs/review_form.html'
    pk_url_kwarg = 'review_id'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете редактировать только свои отзывы')
        return redirect('dogs:photo_list')

    def get_success_url(self):
        return reverse_lazy('dogs:photo_detail', kwargs={'photo_id': self.object.photo.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo'] = self.object.photo
        return context


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'dogs/review_confirm_delete.html'
    pk_url_kwarg = 'review_id'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете удалять только свои отзывы')
        return redirect('dogs:photo_list')

    def get_success_url(self):
        return reverse_lazy('dogs:photo_detail', kwargs={'photo_id': self.object.photo.id})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Отзыв удалён!')
        return super().delete(request, *args, **kwargs)
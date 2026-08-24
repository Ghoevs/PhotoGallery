from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from .models import Dog, Breed, Pedigree, Review
from .forms import DogForm, PedigreeForm, ReviewForm
from .services import send_views_notification
from users.services import send_dog_created_email


class IndexView(TemplateView):
    template_name = 'dogs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Питомник собак'
        return context


class DogListView(ListView):
    model = Dog
    template_name = 'dogs/dogs_list.html'
    context_object_name = 'dogs'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        breed_id = self.request.GET.get('breed')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(breed__name__icontains=query)
            )

        if breed_id:
            queryset = queryset.filter(breed_id=breed_id)

        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breeds'] = Breed.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_breed'] = self.request.GET.get('breed', '')
        return context


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'
    context_object_name = 'dog'
    pk_url_kwarg = 'dog_id'

    def get_object(self, queryset=None):
        dog = super().get_object(queryset)
        if self.request.user != dog.owner:
            dog.views += 1
            dog.save()
            send_views_notification(dog)
        return dog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['review_form'] = ReviewForm()
        return context


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    success_url = reverse_lazy('dogs:dogs_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Добавить'
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        send_dog_created_email(self.request.user, self.object)
        messages.success(self.request, 'Собака добавлена!')
        return response


class DogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dog
    template_name = 'dogs/dog_form.html'
    pk_url_kwarg = 'dog_id'

    def test_func(self):
        dog = self.get_object()
        return self.request.user == dog.owner

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете редактировать только своих собак')
        return redirect('dogs:dogs_list')

    def get_form_class(self):
        return DogForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Изменить'
        return context

    def get_success_url(self):
        return reverse_lazy('dogs:dog_detail', kwargs={'dog_id': self.object.id})


class DogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dog
    template_name = 'dogs/dog_confirm_delete.html'
    pk_url_kwarg = 'dog_id'
    success_url = reverse_lazy('dogs:dogs_list')

    def test_func(self):
        dog = self.get_object()
        return self.request.user == dog.owner

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете удалять только своих собак')
        return redirect('dogs:dogs_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Собака удалена!')
        return super().delete(request, *args, **kwargs)


class BreedListView(ListView):
    model = Breed
    template_name = 'dogs/breeds.html'
    context_object_name = 'breeds'
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


class PedigreeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Pedigree
    form_class = PedigreeForm
    template_name = 'dogs/pedigree_form.html'
    success_url = reverse_lazy('dogs:dogs_list')

    def test_func(self):
        dog = get_object_or_404(Dog, id=self.kwargs['dog_id'])
        return self.request.user == dog.owner

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете добавлять родословную только своим собакам')
        return redirect('dogs:dogs_list')

    def form_valid(self, form):
        dog = get_object_or_404(Dog, id=self.kwargs['dog_id'])
        form.instance.dog = dog
        messages.success(self.request, f'Родословная для {dog.name} добавлена!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dog'] = get_object_or_404(Dog, id=self.kwargs['dog_id'])
        return context


class PedigreeDetailView(DetailView):
    model = Pedigree
    template_name = 'dogs/pedigree_detail.html'
    context_object_name = 'pedigree'

    def get_object(self):
        dog = get_object_or_404(Dog, id=self.kwargs['dog_id'])
        return get_object_or_404(Pedigree, dog=dog)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'dogs/review_form.html'

    def form_valid(self, form):
        dog = get_object_or_404(Dog, id=self.kwargs['dog_id'])
        form.instance.dog = dog
        form.instance.user = self.request.user
        messages.success(self.request, 'Отзыв добавлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dogs:dog_detail', kwargs={'dog_id': self.kwargs['dog_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dog'] = get_object_or_404(Dog, id=self.kwargs['dog_id'])
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
        return redirect('dogs:dogs_list')

    def get_success_url(self):
        return reverse_lazy('dogs:dog_detail', kwargs={'dog_id': self.object.dog.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dog'] = self.object.dog
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
        return redirect('dogs:dogs_list')

    def get_success_url(self):
        return reverse_lazy('dogs:dog_detail', kwargs={'dog_id': self.object.dog.id})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Отзыв удалён!')
        return super().delete(request, *args, **kwargs)

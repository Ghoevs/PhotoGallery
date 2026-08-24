from django.urls import path
from . import views

app_name = 'dogs'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/', views.DogListView.as_view(), name='dogs_list'),
    path('dog/<int:dog_id>/', views.DogDetailView.as_view(), name='dog_detail'),
    path('create/', views.DogCreateView.as_view(), name='dog_create'),
    path('dog/<int:dog_id>/update/', views.DogUpdateView.as_view(), name='dog_update'),
    path('dog/<int:dog_id>/delete/', views.DogDeleteView.as_view(), name='dog_delete'),
    path('breeds/', views.BreedListView.as_view(), name='breeds'),
    path('dog/<int:dog_id>/pedigree/create/', views.PedigreeCreateView.as_view(), name='pedigree_create'),
    path('dog/<int:dog_id>/pedigree/', views.PedigreeDetailView.as_view(), name='pedigree_detail'),
    path('dog/<int:dog_id>/review/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:review_id>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:review_id>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]

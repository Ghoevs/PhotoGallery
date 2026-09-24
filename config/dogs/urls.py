from django.urls import path
from . import views

app_name = 'dogs'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('photos/', views.PhotoListView.as_view(), name='photo_list'),
    path('photos/<int:photo_id>/', views.PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/create/', views.PhotoCreateView.as_view(), name='photo_create'),
    path('photos/<int:photo_id>/update/', views.PhotoUpdateView.as_view(), name='photo_update'),
    path('photos/<int:photo_id>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),
    path('user/<int:user_id>/photos/', views.UserPhotoListView.as_view(), name='user_photos'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('photos/<int:photo_id>/review/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:review_id>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:review_id>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]
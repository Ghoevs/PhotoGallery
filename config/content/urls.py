from django.urls import path
from . import api_views

app_name = 'content'

urlpatterns = [
    path('sections/', api_views.SectionListCreateView.as_view(), name='section_list'),
    path('sections/<int:pk>/', api_views.SectionDetailView.as_view(), name='section_detail'),
    path('contents/', api_views.ContentListCreateView.as_view(), name='content_list'),
    path('contents/<int:pk>/', api_views.ContentDetailView.as_view(), name='content_detail'),
]
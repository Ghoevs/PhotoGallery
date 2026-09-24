from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Section, Content
from .serializers import SectionSerializer, ContentSerializer
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from .paginators import ContentPagination, StandardResultsSetPagination


class SectionListCreateView(generics.ListCreateAPIView):
    queryset = Section.objects.filter(is_active=True)
    serializer_class = SectionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
    ordering = ['title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminOrReadOnly()]
        return [permissions.AllowAny()]


class SectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrReadOnly]


class ContentListCreateView(generics.ListCreateAPIView):
    serializer_class = ContentSerializer
    pagination_class = ContentPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body', 'section__title']
    ordering_fields = ['created_at', 'views', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Content.objects.filter(is_published=True)
        section_id = self.request.query_params.get('section')
        if section_id:
            queryset = queryset.filter(section_id=section_id)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Content.objects.all()
        return Content.objects.filter(is_published=True)

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.author:
            obj.views += 1
            obj.save()
        return obj
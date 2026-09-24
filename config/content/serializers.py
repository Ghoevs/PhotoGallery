from rest_framework import serializers
from .models import Section, Content


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class ContentSerializer(serializers.ModelSerializer):
    section_title = serializers.CharField(source='section.title', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'section', 'section_title', 'body', 'author',
                  'author_username', 'image', 'views', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'views', 'created_at', 'updated_at']
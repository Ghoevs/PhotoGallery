from rest_framework import serializers
from .models import Section, Content, Question


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


class QuestionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    content_title = serializers.CharField(source='content.title', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'content', 'content_title', 'user', 'user_username',
                  'answer', 'is_answered', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'is_answered', 'created_at', 'updated_at']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['answer', 'is_answered']

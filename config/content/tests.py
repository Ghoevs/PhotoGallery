from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from .models import Section, Content, Question


class SectionAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            username='admin',
            password='Admin12345'
        )
        self.user = User.objects.create_user(
            email='user@test.com',
            username='user',
            password='User12345'
        )
        self.section = Section.objects.create(
            title='Тестовый раздел',
            description='Описание тестового раздела',
            is_active=True
        )

    def test_get_sections_list(self):
        response = self.client.get(reverse('content:section_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_section_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'title': 'Новый раздел', 'description': 'Описание'}
        response = self.client.post(reverse('content:section_list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 2)

    def test_create_section_as_user(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Новый раздел'}
        response = self.client.post(reverse('content:section_list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_section(self):
        self.client.force_authenticate(user=self.admin)
        data = {'title': 'Обновленный раздел'}
        response = self.client.patch(reverse('content:section_detail', args=[self.section.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.section.refresh_from_db()
        self.assertEqual(self.section.title, 'Обновленный раздел')

    def test_delete_section(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse('content:section_detail', args=[self.section.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Section.objects.count(), 0)


class ContentAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='author@test.com',
            username='author',
            password='Author12345'
        )
        self.other_user = User.objects.create_user(
            email='other@test.com',
            username='other',
            password='Other12345'
        )
        self.section = Section.objects.create(title='Раздел', is_active=True)
        self.content = Content.objects.create(
            title='Тестовый контент',
            section=self.section,
            body='Тело контента',
            author=self.user,
            is_published=True
        )

    def test_get_contents_list(self):
        response = self.client.get(reverse('content:content_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_content(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Новый контент',
            'section': self.section.id,
            'body': 'Тело нового контента',
            'is_published': True
        }
        response = self.client.post(reverse('content:content_list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Content.objects.count(), 2)
        self.assertEqual(Content.objects.last().author, self.user)

    def test_update_content_by_author(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Обновленный контент'}
        response = self.client.patch(reverse('content:content_detail', args=[self.content.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.content.refresh_from_db()
        self.assertEqual(self.content.title, 'Обновленный контент')

    def test_update_content_by_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        data = {'title': 'Взлом'}
        response = self.client.patch(reverse('content:content_detail', args=[self.content.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_content_by_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('content:content_detail', args=[self.content.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Content.objects.count(), 0)

    def test_content_views_counter(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('content:content_detail', args=[self.content.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.content.refresh_from_db()
        self.assertEqual(self.content.views, 1)


class QuestionAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            username='admin',
            password='Admin12345'
        )
        self.user = User.objects.create_user(
            email='user@test.com',
            username='user',
            password='User12345'
        )
        self.section = Section.objects.create(title='Раздел', is_active=True)
        self.content = Content.objects.create(
            title='Контент',
            section=self.section,
            body='Тело',
            author=self.user,
            is_published=True
        )
        self.question = Question.objects.create(
            text='Тестовый вопрос',
            user=self.user,
            content=self.content
        )

    def test_get_questions_list(self):
        response = self.client.get(reverse('content:question_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_question(self):
        self.client.force_authenticate(user=self.user)
        data = {'text': 'Новый вопрос', 'content': self.content.id}
        response = self.client.post(reverse('content:question_list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_answer_question_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'answer': 'Ответ на вопрос', 'is_answered': True}
        response = self.client.patch(reverse('content:question_detail', args=[self.question.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertTrue(self.question.is_answered)
        self.assertEqual(self.question.answer, 'Ответ на вопрос')

    def test_delete_question_by_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('content:question_detail', args=[self.question.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)

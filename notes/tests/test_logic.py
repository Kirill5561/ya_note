from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

# Импортируем из файла с формами список стоп-слов и предупреждение формы.
# Загляните в news/forms.py, разберитесь с их назначением.
from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):
	
	COMMENT_TEXT = 'Текст'


    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Автор')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.url = reverse('notes:add')
        cls.form_data = {'title': cls.COMMENT_TEXT,
                         'text': cls.COMMENT_TEXT,
                         'slug': 'new-slug'}

    def test_user_can_create_note(self):
        # Совершаем запрос через авторизованный клиент.
        response = self.auth_client.post(self.url, data=self.form_data)
        # Проверяем, что редирект привёл к разделу с комментами.
        self.assertRedirects(response, reverse('notes:success'))
        # Считаем количество комментариев.
        note_count = Note.objects.count()
        # Убеждаемся, что есть один комментарий.
        self.assertEqual(note_count, 1)
        # Получаем объект комментария из базы.
        note = Note.objects.get()
        # Проверяем, что все атрибуты комментария совпадают с ожидаемыми.
        self.assertEqual(note.text, self.COMMENT_TEXT)
        self.assertEqual(note.title, self.COMMENT_TEXT)
        self.assertEqual(note.slug, 'new-slug')
        self.assertEqual(note.author, self.user)


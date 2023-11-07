from http import HTTPStatus

# Импортируем функцию для определения модели пользователя.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Импортируем класс комментария.
from notes.models import Note
 
# Получаем модель пользователя.
User = get_user_model()

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=cls.author,)

    def test_pages_availability_for_anonymous_user(self):
        urls = ('notes:home', 'users:login', 'users:logout', 'users:signup')
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)


    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=cls.author,)

    def test_pages_availability_for_auth_user(self):
        urls = ('notes:list', 'notes:add', 'notes:success')
        self.client.force_login(self.author)
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)


    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=cls.author,)

    def test_pages_availability_for_different_users(self):
        users_statuses = (
        	(self.reader, HTTPStatus.NOT_FOUND),
            (self.author, HTTPStatus.OK),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:detail', 'notes:edit', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)



    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=cls.author,)


    def test_redirects(self):
        urls = (
        ('notes:detail', (self.note.slug,)),
        ('notes:edit', (self.note.slug,)),
        ('notes:delete', (self.note.slug,)),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
        )

        for name, args in urls:
            with self.subTest(name=name):
                login_url = reverse('users:login')
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)




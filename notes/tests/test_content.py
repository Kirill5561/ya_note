from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    COMMENT_TEXT = 'Текст'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Автор')
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст заметки',
                                       slug='note-slug',
                                       author=cls.user,)
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.form_data = {'title': cls.COMMENT_TEXT,
                         'text': cls.COMMENT_TEXT,
                         'slug': 'note-slug'}

    def test_note_in_list_for_author(self):
        url = reverse('notes:list')
        response = self.auth_client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_not_in_list_for_another_user(self):
        url = reverse('notes:list')
        response = self.reader_client.get(url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', slug='title', author=cls.author
        )

    def test_pages_availability(self):
        names = (
            'notes:home', 'users:login', 'users:logout', 'users:signup'
        )
        for name in names:
            with self.subTest(name=name):
                url = reverse('notes:home')
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_done_done(self):
        for name in ('notes:list', 'notes:success', 'notes:add'):
            self.client.force_login(self.author)
            with self.subTest(name=name):
                url = reverse('notes:list')
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_detail_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND)
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:detail', 'notes:edit', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, kwargs={'slug': self.note.slug})
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        note_slug = {'slug': self.note.slug}
        names_kwargs = (
            ('notes:edit', note_slug),
            ('notes:delete', note_slug),
            ('notes:detail', note_slug),
            ('notes:list', None),
            ('notes:add', None),
            ('notes:success', None)
        )
        for name, kwargs in names_kwargs:
            with self.subTest(name=name):
                url = reverse(name, kwargs=kwargs)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

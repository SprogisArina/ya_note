from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author1 = User.objects.create(username='Автор1')
        cls.author1_client = Client()
        cls.author1_client.force_login(cls.author1)
        cls.author2 = User.objects.create(username='Автор2')
        cls.note1 = Note.objects.create(
            title='Заголовок', text='Текст', slug='title1', author=cls.author1
        )
        cls.note2 = Note.objects.create(
            title='Заголовок', text='Текст', slug='title2', author=cls.author2
        )

    def test_list_content(self):
        response = self.author1_client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertIsNot(self.note2, object_list)
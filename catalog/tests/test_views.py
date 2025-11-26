from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from catalog.models import Author, Book, BookInstance, UserBookStatus

class CatalogViewsTest(TestCase):
    def setUp(self):
        # Создаём тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Создаём автора и книгу
        author = Author.objects.create(first_name="Agatha", last_name="Christie")
        book = Book.objects.create(title="Murder on the Orient Express", author=author, isbn="978-0-061-23456-7")

        # Создаём экземпляр книги, выданной пользователю
        BookInstance.objects.create(book=book, borrower=self.user, status='o', imprint="First Edition")

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Добро пожаловать в Local Library!')

    def test_book_list_view(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Murder on the Orient Express')

    def test_login_required_for_mybooks(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/mybooks/')

    def test_user_can_see_their_books_after_login(self):
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login)

        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Murder on the Orient Express')
from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import Author, Book, BookInstance, UserBookStatus

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='John', last_name='Doe')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(first_name='Jane', last_name='Austen')
        Book.objects.create(title='Pride and Prejudice', author=author, isbn='978-0-123456-78-9')

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_object_name_is_title(self):
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), book.title)

class BookInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        author = Author.objects.create(first_name='Leo', last_name='Tolstoy')
        book = Book.objects.create(title='War and Peace', author=author, isbn='978-1-234567-89-0')
        BookInstance.objects.create(book=book, imprint='First Edition', borrower=user)

    def test_object_name_is_book_imprint_id(self):
    # Создаём автора, книгу и экземпляр книги
        author = Author.objects.create(first_name="Test", last_name="Author")
        book = Book.objects.create(title="Test Book", author=author, isbn="978-0-123456-78-9")
        book_instance = BookInstance.objects.create(book=book, imprint="First Edition")

        expected_object_name = f'{book_instance.id} ({book_instance.book.title})'       
        self.assertEqual(str(book_instance), expected_object_name)

class UserBookStatusModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        author = Author.objects.create(first_name='Mark', last_name='Twain')
        book = Book.objects.create(title='Tom Sawyer', author=author, isbn='978-0-987654-32-1')
        book_instance = BookInstance.objects.create(book=book, imprint='Second Edition', borrower=user)
        UserBookStatus.objects.create(user=user, book_instance=book_instance, is_read=True, is_favorite=False)

    def test_object_name(self):
        status = UserBookStatus.objects.get(id=1)
        expected_name = f"{status.user.username} — {status.book_instance.book.title}"
        self.assertEqual(str(status), expected_name)

    def test_is_read_default(self):
        status = UserBookStatus.objects.get(id=1)
        self.assertTrue(status.is_read)
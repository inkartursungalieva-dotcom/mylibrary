from django.test import TestCase
from catalog.forms import RenewBookForm, UserBookStatusForm
from datetime import date, timedelta

class RenewBookFormTest(TestCase):
    def test_renewal_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renewal_date'].label is None or form.fields['renewal_date'].label == 'renewal date')

    def test_renewal_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Введите дату возврата (до 4 недель от сегодня)')

    def test_renewal_date_in_past(self):
        date_past = date.today() - timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date_past})
        self.assertFalse(form.is_valid())

    def test_renewal_date_too_far_in_future(self):
        date_future = date.today() + timedelta(weeks=5)
        form = RenewBookForm(data={'renewal_date': date_future})
        self.assertFalse(form.is_valid())

    def test_renewal_date_today(self):
        date_today = date.today()
        form = RenewBookForm(data={'renewal_date': date_today})
        self.assertTrue(form.is_valid())

    def test_renewal_date_max_4_weeks(self):
        date_in_4_weeks = date.today() + timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date_in_4_weeks})
        self.assertTrue(form.is_valid())

class UserBookStatusFormTest(TestCase):
    def test_form_has_fields(self):
        form = UserBookStatusForm()
        expected_fields = {'is_read', 'is_favorite'}
        actual_fields = set(form.fields.keys())
        self.assertEqual(expected_fields, actual_fields)
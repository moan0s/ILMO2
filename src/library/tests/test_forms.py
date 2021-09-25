from django.test import SimpleTestCase
from django.utils import timezone
from library.forms import RenewBookForm
import datetime

class RenewBookTests(SimpleTestCase):
    def test_correct_renew(self):
        renewal_date = datetime.date.today() + datetime.timedelta(days=20)
        form_data = {'renewal_date': str(renewal_date)}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_to_late_renew(self):
        renewal_date = datetime.date.today() + datetime.timedelta(days=40)
        form_data = {'renewal_date': str(renewal_date)}
        form = RenewBookForm(data=form_data)
        self.assertEqual(form.errors['renewal_date'][0],
            'Invalid date - renewal more than 4 weeks ahead')
        self.assertFalse(form.is_valid())

    def test_past_renew(self):
        renewal_date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': str(renewal_date)}
        form = RenewBookForm(data=form_data)
        self.assertEqual(form.errors['renewal_date'][0],
            'Invalid date - renewal in past')
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

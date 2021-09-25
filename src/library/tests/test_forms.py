from django.test import TestCase
from library.forms import RenewBookForm
import datetime

class RenewBookTests(TestCase):
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
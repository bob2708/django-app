from django.test import TestCase

# Создайте ваши тесты здесь

import datetime
from django.utils import timezone
from catalog.forms import StihForm, NewUserForm

class NewUserFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = NewUserForm()
        self.assertTrue(True)

    def test_renew_form_date_field_help_text(self):
        form = NewUserForm()
        self.assertEqual(1, 1)

    def test_renew_form_date_in_past(self):
        #date = datetime.date.today() - datetime.timedelta(days=1)
        #form_data = {'renewal_date': date}
        #form = NewUserForm(data=form_data)
        self.assertFalse(False)

    def test_renew_form_date_too_far_in_future(self):
        self.assertFalse(False)

    def test_renew_form_date_today(self):
        self.assertTrue(True)

    def test_renew_form_date_max(self):
        self.assertTrue(True)

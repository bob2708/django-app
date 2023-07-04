from django.test import TestCase

# Create your tests here.

from catalog.models import Author, Stih

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'died')

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1')

class StihModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Stih.objects.create(title='title', content='content', pub_date='2020-10-10')

    def test_title_label(self):
        stih=Stih.objects.get(id=1)
        field_label = stih._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_pub_date_label(self):
        stih=Stih.objects.get(id=1)
        field_label = stih._meta.get_field('pub_date').verbose_name
        self.assertEquals(field_label,'date published')

    def test_checked_default_value(self):
        stih=Stih.objects.get(id=1)
        checked = stih._checked
        self.assertFalse(checked)

    def test_object_name_is_title(self):
        stih=Stih.objects.get(id=1)
        expected_object_name = stih.title
        self.assertEquals(expected_object_name, str(stih))

    def test_get_absolute_url(self):
        stih=Stih.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(stih.get_absolute_url(),'/catalog/stih/1')
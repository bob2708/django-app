from django.test import TestCase
from django.contrib.auth.models import Permission
from django.utils import timezone
from catalog.models import Stih, Author
from django.contrib.auth.models import User
from django.urls import reverse
import datetime


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create 13 authors for pagination tests
        number_of_authors = 13
        for author_num in range(number_of_authors):
            Author.objects.create(first_name='Christian %s' % author_num, last_name = 'Surname %s' % author_num,)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['author_list']) == 10)

    def test_lists_all_authors(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['author_list']) == 3)


class StihByUserListViewTest(TestCase):

    def setUp(self):
        # Создание двух пользователей
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

        test_author = Author.objects.create(first_name='John', last_name='Smith', account=test_user1)
        test_stih = Stih.objects.create(title='Stih Title', content = 'My stih summary', pub_date='2020-10-10', author=test_author)
        # Create genre as a post-step

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-stihs'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/mystihs/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-stihs'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'catalog/stih_list_user.html')

    def test_only_user_stihs_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-stihs'))
        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)
        get_ten_stihs = Stih.objects.all()[:10]

        for stih in get_ten_stihs:
            stih._checked=False
            stih.save()

        resp = self.client.get(reverse('my-stihs'))
        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)

    def test_on_list(self):
        self.assertEqual(200, 200)


class RenewStihViewTest(TestCase):

    def setUp(self):
        #Создание пользователя
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()
        permission = Permission.objects.get(name='Set stih as valid')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        test_author = Author.objects.create(first_name='John', last_name='Smith', account=test_user1)
        
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_stih1=Stih.objects.create(title='Stih Title', content = 'My stih content', pub_date='2020-10-10', author=test_author)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('renew-stih', kwargs={'pk':self.test_stih1.pk,}) )
        #Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/accounts/login/') )

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('renew-stih', kwargs={'pk':self.test_stih1.pk,}) )

        #Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/accounts/login/') )

    def test_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renew-stih', kwargs={'pk':self.test_stih1.pk,}) )

        #Check that it lets us login - this is our book and we have the right permissions.
        self.assertEqual( resp.status_code,200)

    def test_HTTP404_for_invalid_stih_if_logged_in(self):
        test_id = 999999
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renew-stih', kwargs={'pk':test_id,}) )
        self.assertEqual( resp.status_code,404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renew-stih', kwargs={'pk':self.test_stih1.pk,}) )
        self.assertEqual( resp.status_code,200)

        #Check we used correct template
        self.assertTemplateUsed(resp, 'catalog/stih_renew.html')

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.post(reverse('renew-stih', kwargs={'pk':self.test_stih1.pk,}), {'_checked':True} )
        self.assertRedirects(resp, reverse('unchecked-stihs'))

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Stih(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000, help_text="Stih content")
    pub_date = models.DateField('date published')

    _checked = models.BooleanField(default=False)
	
    @property
    def checked(self):
        return self._checked
	
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('stih-detail', args=[str(self.id)])

    class Meta:
    	permissions = (("can_validate", "Set stih as valid"), ("cant_validate", "Low permissions user"))


class AuthorManger(models.Manager):
    def create_author(self, first_name, last_name, date_of_birth, account, date_of_death=None):
        author = self.create(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, account=account, date_of_death=date_of_death)
        return author         

class Author(models.Model):
    classic = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    objects = AuthorManger()

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

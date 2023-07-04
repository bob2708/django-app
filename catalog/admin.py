from django.contrib import admin

# Register your models here.
from .models import Author, Stih 

#admin.site.register(Author)
#admin.site.register(Stih)

# Register the Admin classes for Book using the decorator
@admin.register(Stih)
class StihAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'checked')

class StihInstanceInline(admin.TabularInline):
    model = Stih

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death', 'account', 'classic')
    fields = ['first_name', 'last_name', 'account', ('date_of_birth', 'date_of_death'), 'classic']
    inlines = [StihInstanceInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)



    

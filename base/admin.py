from django.contrib import admin
from .models import *
# Register your models here.

class BookRentalAdmin(admin.ModelAdmin):
    search_fields = ['user__profile__readerCard']

class AuthorAdmin(admin.ModelAdmin):
    fields = ['name'] 

class TopicAdmin(admin.ModelAdmin):
    fields = ['name'] 

class PublisherAdmin(admin.ModelAdmin):
    fields = ['name'] 

# class BookAdmin(admin.ModelAdmin):
#     search_fields = ['bookID']

admin.site.register(Topic, TopicAdmin)
admin.site.register(Position)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(BookRental, BookRentalAdmin)
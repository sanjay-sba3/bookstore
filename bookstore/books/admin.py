from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Rating, Category


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Rating)

# Register your models here.

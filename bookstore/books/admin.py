from django.contrib import admin
from .models import User, Book, Rating, Category


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Rating)

# Register your models here.

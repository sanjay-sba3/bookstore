from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager



# Create your models here

#Model for Custom User Table
class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    object = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username

# Model for Category of books in store
class Category(models.Model):
    name = models.CharField(max_length=255)  

    class Mata:
        db_table = 'category_master'

    
# Model for Books in store
class Book(models.Model):
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    

    class Meta:
        db_table = 'books_master'
            
# Model for Rating given by users to books
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        db_table = 'Rating'
# Create your models here.

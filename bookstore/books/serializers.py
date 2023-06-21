from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    def validate_rating(self,value):
        if value > 5:
            raise serializers.ValidationError("give rating out of 5.....")
        return value
    class Meta:
        model = Rating
        fields = '__all__'
from django.urls import path, include
from . import views



urlpatterns = [
   
    path('books/', views.BookViews.as_view(), ),
    path('books/<int:id>', views.BookViews.as_view(), ),
    path('category/', views.CategoryViews.as_view(), ),
    path('category/<int:id>', views.CategoryViews.as_view(), ),
    path('user/', views.UserViews.as_view(), ),
    path('user/<int:id>', views.UserViews.as_view(), ),
    path('rating/', views.RatingViews.as_view(), ),
    path('rating/<int:id>', views.RatingViews.as_view()),
    path('login/', views.LoginView.as_view(), ),
    path('user_list/', views.UserListAPIView.as_view(), )
]
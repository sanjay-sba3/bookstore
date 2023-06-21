from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import BooksSerializer, UserSerializer, RatingSerializer, CategorySerializer
from .models import User, Book, Rating, Category
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import logging,traceback
logger = logging.getLogger('django')


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# Login using Valid Username and Password 
class LoginView(APIView):
    def post(self, request):
        loginuser = request.data['username']
        loginpass = request.data['password']
        user = authenticate(username=loginuser, password=loginpass)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"token" : token, "response": 'Successfuly logged in....'})
        else:
            return Response({"response":f"{loginuser} not found"})

class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

# CRUD Oparation for Books
class BookViews(ListAPIView):
    authentication_Classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()                     # fatching data
    serializer_class = BooksSerializer                 # Use rto serializer for data fatched  
    filter_backends = [SearchFilter]
    search_fields = ['User.id','Category.name']


    def get(self, request, id = None):
        
        logger.info("this is books get request")
        logger.debug("this is degubing info")
        if id == None:    
            book = Book.objects.all()
            serializer = BooksSerializer(book, many = True)
            return Response(serializer.data)
        else:
            try:
                book = Book.objects.get(id=id)
            except Book.DoesNotExist:
                return Response({"status" : "ID for book dose not exists..."}) 
            else:

                rating = Rating.objects.filter(book=id)
                serializer_rating = RatingSerializer(rating, many = True)

                books = Book.objects.all()
                serializer_books = BooksSerializer(books, many= True)
                            
                r = []
                for i in range (len(serializer_rating.data)): 
                    if serializer_rating.data[i]["book"] == id: 
                        
                        rating_list = serializer_rating.data[i]["rating"]
                        
                        r.append(rating_list)
                try:
                    book = Book.objects.filter(id=id)        
                    sum = 0
                    for j in r:
                        sum +=j
                    ave = sum/len(r)  
                except ZeroDivisionError:
                    
                    serializer = BooksSerializer(book, many= True)
                    return Response({"Book":serializer.data[0]["title"],"author": serializer.data[0]["author"],"avarage Rating":"No retings for Book ....."})
                else:
                    
                    serializer = BooksSerializer(book, many= True)
                    return Response({"Book":serializer.data[0]["title"],"author": serializer.data[0]["author"],"avarage Rating": ave})
            
    def post(self, request):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.save()
            return Response({
                              "status": "status.HTTP_201_succes",
                              "type": "success",
                              "message": "data uploaded successfully.... ",
                              "data": [serializer.data],
                              })  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def put(self, request, id):
      try:
            book = Book.objects.get(id=id)              
      except Book.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND,
                                    "type": "success",
                                    "message": "data not fond",
                            })  
            
      serializer = BooksSerializer(book,data=request.data)       
      if serializer.is_valid():
            serializer.save()
            return Response( {"status": "status.HTTP_",
                                    "type": "success",
                                    "message": "data updated successfully..... ",
                                    "data": serializer.data,
                                    })
            
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                    
    def delete(self, request, id):
            try:
                  book = Book.objects.get(id=id)
            except Book.DoesNotExist:
                   return Response({"status": status.HTTP_404_NOT_FOUND,
                                    "type": "success",
                                    "message": "data not fond",
                                   })
            
            book.delete()
            return Response({"status": "204",
                              "type": "success",
                              "message": "data deleted successfully..... ",
                              "data": status.HTTP_204_NO_CONTENT,
                                })
                              

# CRUD Oparation for Category
class CategoryViews(ListAPIView):
    authentication_Classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, id = None):
        if id == None: 
               
            category = Category.objects.all()
            serializer = CategorySerializer(category, many = True)
            return Response(serializer.data)
        else:
            try:
                category = Category.objects.filter(id =id)
            except Category.DoesNotExist:
                return Response({"status" : "Category for book dose not exists..."})   
            else:
                category = Category.objects.all()
                serializer = CategorySerializer(category, many = True)
                book = Book.objects.filter(category=id)
                serializer_book = BooksSerializer(book, many = True)
                for i in serializer.data:
                     if i["id"]==id:
                          cat = i['name']
                return Response({"Category":cat, "titles": [x["title"] for x in serializer_book.data]})
                # return Response(serializer.data)
            
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.save()
            return Response({
                              "status": "status.HTTP_201_succes",
                              "type": "success",
                              "message": "data uploaded successfully.... ",
                              "data": [serializer.data],
                              })  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def put(self, request, id):
      try:
            category = Category.objects.get(id=id)
                  
      except Category.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND,
                                    "type": "success",
                                    "message": "data not fond",
                            })  
            
      serializer = CategorySerializer(category,data=request.data) 
            
      if serializer.is_valid():
            serializer.save()
            return Response( {"status": "status.HTTP_",
                                    "type": "success",
                                    "message": "data updated successfully..... ",
                                    "data": serializer.data,
                                    })
      
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                                    
    def delete(self, request, id):
            try:
                  category = Category.objects.get(id=id)
            except Category.DoesNotExist:
                   return Response({"status": status.HTTP_404_NOT_FOUND,
                                    "type": "success",
                                    "message": "data not fond",
                                   })
            
            category.delete()
            return Response({"status": "204",
                              "type": "success",
                              "message": "data deleted successfully..... ",
                              "data": status.HTTP_204_NO_CONTENT,
                                })

# CRUD Oparation for users
class UserViews(ListAPIView):

    authentication_Classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, id = None):
        if id == None:    
            user = User.objects.all()
            serializer = UserSerializer(user, many = True)
            return Response(serializer.data)
        else:
            try:
                user = User.objects.filter(id=id)
            except User.DoesNotExist:
                return Response({"status" : "User dose not exists..."})   
            else:
                user = User.objects.all()
                serializer = UserSerializer(user, many = True)
                book = Book.objects.filter(user=id)
                serializer_book = BooksSerializer(book, many = True)
                return Response({"Username":serializer.data[0]["username"], "titles": [x["title"] for x in serializer_book.data]})
            
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.save()
            return Response({
                              "status": "status.HTTP_201_succes",
                              "type": "success",
                              "message": "data uploaded successfully.... ",
                              "data": [serializer.data],
                              })  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def put(self, request, id):
      try:
            user = User.objects.get(id=id)
                  
      except User.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND,
                                    "type": "success",
                                    "message": "data not fond",
                            })  
            
      serializer = UserSerializer(user,data=request.data) 
            
      if serializer.is_valid():
            serializer.save()
            return Response( {"status": "status.HTTP_",
                                    "type": "success",
                                    "message": "data updated successfully..... ",
                                    "data": serializer.data,
                                    })
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                    
    def delete(self, request, id):
            try:
                  user = User.objects.get(id=id)
            except User.DoesNotExist:
                   return Response({"status": status.HTTP_404_NOT_FOUND,
                                    "type": "success",
                                    "message": "data not fond",
                                   })
            
            User.delete()
            return Response({"status": "204",
                              "type": "success",
                              "message": "data deleted successfully..... ",
                              "data": status.HTTP_204_NO_CONTENT,
                                })

# CRUD Oparation for ratings
class RatingViews(APIView):
    authentication_Classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request, id = None):
        if id == None:    
            rating = Rating.objects.all()
            serializer = RatingSerializer(rating, many = True)
            return Response(serializer.data)
        else:
            try:
                user = User.objects.get(id=id)
                # rating = Rating.objects.filter(id=id)
            except User.DoesNotExist:
                return Response({"status" : "User with Rating for book dose not exists..."})   
            else:
                rating = Rating.objects.filter(user=id)
                serializer_rating = RatingSerializer(rating, many = True)

                user = User.objects.filter(id=serializer_rating.data[0]["user"])
                serializer_user = UserSerializer(user, many = True)
                
                books = Book.objects.all()
                serializer_books = BooksSerializer(books, many= True)
                l = []
                r = []
                for i in range (len(serializer_rating.data)): 
                    if serializer_rating.data[i]["user"] == id: 
                        book_list = serializer_books.data[serializer_rating.data[i]["book"]-1]["title"]
                        rating_list = serializer_rating.data[i]["rating"]
                        l.append(book_list)
                        r.append(rating_list)
                        rating = [dict(zip(l,r))]
                
                        
        return Response({"Username":f"{serializer_user.data[0]['username']} with ID {serializer_user.data[0]['id']}" ,"title with ratings": rating} )

                    # return Response({"responce":"bad request"} )
            
    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.save()
            return Response({
                              "status": "status.HTTP_201_succes",
                              "type": "success",
                              "message": "data uploaded successfully.... ",
                              "data": [serializer.data],
                              })  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def put(self, request, id):
      try:
            rating = Rating.objects.get(id=id)
                  
      except Rating.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND,
                                    "type": "success",
                                    "message": "data not fond",
                            })  
            
      serializer = RatingSerializer(rating,data=request.data) 
            
      if serializer.is_valid():
            serializer.save()
            return Response( {"status": "status.HTTP_",
                                    "type": "success",
                                    "message": "data updated successfully..... ",
                                    "data": serializer.data,
                                    })
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                    
    def delete(self, request, id):
            try:
                  rating = Rating.objects.get(id=id)
            except Rating.DoesNotExist:
                   return Response({"status": status.HTTP_404_NOT_FOUND,
                                    "type": "success",
                                    "message": "data not fond",
                                   })
            
            Rating.delete()
            return Response({"status": "204",
                              "type": "success",
                              "message": "data deleted successfully..... ",
                              "data": status.HTTP_204_NO_CONTENT,
                                })
# Create your views here.

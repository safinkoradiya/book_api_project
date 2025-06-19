from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list_create, name='book-list-create'),
    path('books/<int:pk>/', views.book_detail, name='book-detail'),
    path('books/<int:pk>/upload-cover/', views.upload_cover, name='upload-cover')  
]

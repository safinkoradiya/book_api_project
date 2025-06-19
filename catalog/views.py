from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .models import Book
from .serializers import BookSerializer
from .decorators import require_api_key  # 👈 make sure this exists

# GET (no auth), POST (auth)
@api_view(['GET', 'POST'])
def book_list_create(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        return create_book(request)

@require_api_key
def create_book(request):
    serializer = BookSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET (no auth), PUT/DELETE (auth)
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'GET':
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        return update_book(request, book)

    elif request.method == 'DELETE':
        return delete_book(book)

@require_api_key
def update_book(request, book):
    serializer = BookSerializer(book, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@require_api_key
def delete_book(book):
    book.delete()
    return Response({'message': 'Book deleted'}, status=status.HTTP_204_NO_CONTENT)

# ✅ Upload Cover Image
@api_view(['POST'])
@parser_classes([MultiPartParser])
@require_api_key
def upload_cover(request, pk):
    book = get_object_or_404(Book, pk=pk)

    file = request.FILES.get('cover')

    if not file:
        return Response({
            "error": "NO_FILE",
            "message": "No file was uploaded"
        }, status=400)

    if file.size > 2 * 1024 * 1024:
        return Response({
            "error": "FILE_TOO_LARGE",
            "message": "Max allowed size is 2MB"
        }, status=413)

    ext = file.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
        return Response({
            "error": "INVALID_FILE_TYPE",
            "message": "Only JPG, PNG, and WEBP files are allowed",
            "allowed_types": ["jpg", "png", "webp"],
            "received_type": ext
        }, status=400)

    book.cover_image = file
    book.save()

    return Response({
        "id": book.id,
        "title": book.title,
        "cover_url": request.build_absolute_uri(book.cover_image.url),
        "message": "Cover uploaded successfully"
    })

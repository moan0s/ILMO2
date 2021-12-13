from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from library.models import Book, Member, Room
from .serializers import BookSerializer, AccessSerializer, Access


class BookApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all the books
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the book
        """
        data = {
            'title': request.data.get('title'),
        }
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessControlApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Check if a user has permission to access room
        """
        user = Member.objects.get(UID=kwargs["uk"]).user
        access_bool = Room.objects.get(id=kwargs["rk"]).check_access(user)
        access = Access(access_bool)
        serializer = AccessSerializer(access)
        if access_bool:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)

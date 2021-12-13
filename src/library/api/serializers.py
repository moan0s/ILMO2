from rest_framework import serializers
from library.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author"]


class Access(object):
    def __init__(self, access):
        self.access = access


class AccessSerializer(serializers.Serializer):
    access = serializers.BooleanField()

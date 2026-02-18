from rest_framework import serializers
from .models import Author, Book, Member, BorrowRecord,Review
from django.contrib.auth import get_user_model

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class SimpleUserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = get_user_model()
        fields = ['id','name']
        
    def get_current_user_name(self,obj):
        return obj.get_full_name()
        
        
class ReviewSerializer(serializers.ModelSerializer):
    # user=SimpleUserSerializer()
    user=serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields=['user']
    def get_user(self,obj):
        return SimpleUserSerializer(obj.user).data
    
    def create(self,validated_data):
        book_id=self.context['book_id']
        return Book.objects.filter(book_id=book_id,**validated_data)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = '__all__'

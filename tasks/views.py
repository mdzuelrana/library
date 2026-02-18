from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,AllowAny,DjangoModelPermissions,IsAuthenticated
from django.utils.timezone import now
from tasks.permissions import IsAdminOrReadOnly,IsReviewAuthorOrReadOnly,IsLibrarianOrReadOnly
from .models import Author, Book, Member, BorrowRecord
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowRecordSerializer,ReviewSerializer
# Create your views here.



class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    #permission_classes=[IsAdminOrReadOnly,IsLibrarianOrReadOnly]
    # permission_classes=[DjangoModelPermissions]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]   
        return [IsAuthenticated()] 


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes=[IsAuthenticated]

    @action(detail=False, methods=['post'])
    def borrow(self, request):
        book_id = request.data.get('book')
        member_id = request.data.get('member')

        try:
            book = Book.objects.get(id=book_id)
            member = Member.objects.get(id=member_id)
        except (Book.DoesNotExist, Member.DoesNotExist):
            return Response({"error": "Invalid book or member ID"}, status=400)

        if not book.availability_status:
            return Response({"error": "Book is not available"}, status=400)

        book.availability_status = False
        book.save()

        record = BorrowRecord.objects.create(book=book, member=member)

        return Response(BorrowRecordSerializer(record).data, status=201)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        record_id = request.data.get('borrow_record_id')

        try:
            record = BorrowRecord.objects.get(id=record_id)
        except BorrowRecord.DoesNotExist:
            return Response({"error": "Invalid record ID"}, status=400)

        if record.return_date:
            return Response({"error": "Book already returned"}, status=400)

        record.return_date = now().date()
        record.save()

        book = record.book
        book.availability_status = True
        book.save()

        return Response({"message": "Book returned successfully"})
    
    
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class=ReviewSerializer
    permission_classes=[IsReviewAuthorOrReadOnly]
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self,serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return Book.objects.filter(book_id=self.kwargs['book_pk'])
    def get_serializer_context(self):
        return {'book_id':self.kwargs['book_pk']}

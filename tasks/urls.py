from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, MemberViewSet, BorrowRecordViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('members', MemberViewSet)
router.register('borrow-records', BorrowRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

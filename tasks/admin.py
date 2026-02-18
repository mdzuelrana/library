from django.contrib import admin
from tasks.models import Author,Book,BorrowRecord,Member
# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BorrowRecord)
admin.site.register(Member)

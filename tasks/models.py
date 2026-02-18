from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    ISBN = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    ratings=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    
    def __str__(self):
        return f'Review by {self.user.first_name} on {self.book.title}'
    
    
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrow_records')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.name} borrowed {self.book.title}"

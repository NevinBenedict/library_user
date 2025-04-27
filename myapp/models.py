from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    bio = models.TextField(blank=True,null=True)
    birth_date = models.DateField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    authors =models.ManyToManyField(Author, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField(null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    
    STATUS_CHOICES = (
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')

class LateFee(models.Model):
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE, related_name='late_fee')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
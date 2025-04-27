from django.shortcuts import render,redirect
from django.views.generic import View,CreateView
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
class Register(View):
    def get(self,request):
        form = Userform
        return render(request,"register.html",{'form':form})
    def post(self,request):
        form=Userform(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("login")
        form = Userform
        return render(request,"register.html",{'form':form})
    
class Login(View):
    def get(self,request):
        return render(request,"login.html")
    def post (self,request):
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            print(request.user)
        return redirect("book_list")


class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'isbn', 'authors', 'category', 'publication_date', 'total_copies', 'available_copies', 'cover_image']
    template_name = 'book_form.html'
    success_url = reverse_lazy('login')  # Redirect to the book list page after successful creation

    def form_valid(self, form):
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'book_list.html', {'books': books})

@method_decorator(login_required, name='dispatch')
class BookDetailView(View):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        user = request.user
        is_borrowed = Borrowing.objects.filter(user=user, book=book, return_date__isnull=True).exists()
        if is_borrowed:
            return render(request, 'book_detail.html', {'book': book, 'is_borrowed': True})
        return render(request, 'book_detail.html', {'book': book, 'is_borrowed': False})

class BorrowingcreateView(View):
    def post(self,request,pk):
        book = Book.objects.get(pk=pk)
        user = request.user
        is_borrowed = Borrowing.objects.filter(user=user, book=book, return_date__isnull=True).exists()
        if is_borrowed:
            return render(request, 'book_detail.html', {'book': book, 'error': 'Already borrowed'})
        if book.available_copies > 0:
            due_date = timezone.now() + timezone.timedelta(days=7)  # Set due date to 14 days from now
            Borrowing.objects.create(user=user, book=book, due_date=due_date)
            book.available_copies -= 1
            book.save()
            return redirect('book_detail', pk=pk)  # Redirect to the book detail page after borrowing
        else:
            return render(request, 'book_detail.html', {'book': book, 'error': 'No available copies'})
        
class ReturnBook(View):
    def post(self,request,pk):
        book = Book.objects.get(pk=pk)
        user = request.user
        borrowing = Borrowing.objects.get(user=user, book=book, return_date__isnull=True)
        borrowing.return_date = timezone.now()
        borrowing.save()
        book.available_copies += 1
        book.save()
        if borrowing.return_date>= borrowing.due_date:
            # Handle late return (optional)
            late_fee = (borrowing.return_date - borrowing.due_date).days * 1
            late_fee_obj = LateFee.objects.create(borrowing=borrowing, amount=late_fee)
        
        return redirect('book_list')

class BorrowingListView(View):
    def get(self, request):
        user = request.user
        borrowings = Borrowing.objects.filter(user=user, return_date__isnull=True)
        return render(request, 'borrowing_list.html', {'borrowings': borrowings})
    
class LatefeeListView(View):
    def get(self, request):
        user = request.user
        late_fees = LateFee.objects.filter(borrowing__user=user, paid=False)
        return render(request, 'late_fee_list.html', {'late_fees': late_fees})

class LateFeePaymentView(View):
    def post(self, request, pk):
        late_fee = LateFee.objects.get(pk=pk)
        late_fee.paid = True
        late_fee.payment_date = timezone.now()
        late_fee.save()
        return redirect('late_fee_list')
    
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("login")

class HistoryView(View):
    def get(self,request):
        user = request.user
        borrowings = Borrowing.objects.filter(user=user).exclude(return_date__isnull=True)
        return render(request, 'history.html', {'borrowings': borrowings})
    
class FeeHistoryView(View):
    def get(self,request):
        user = request.user
        late_fees = LateFee.objects.filter(borrowing__user=user, paid=True)
        return render(request, 'fee_history.html', {'late_fees': late_fees})
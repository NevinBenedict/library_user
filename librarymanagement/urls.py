"""
URL configuration for librarymanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',Register.as_view(),name="register"),
    path('login/',Login.as_view(),name="login"),
    path('book/create/', BookCreateView.as_view(), name='book_create'),  
    path('book/list/', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/borrow/', BorrowingcreateView.as_view(), name='borrow_book'),
    path('book/<int:pk>/return/', ReturnBook.as_view(), name='return_book'),  # Add this line for the return book view
    path('borrowings/', BorrowingListView.as_view(), name='borrowing_list'),  # Add this line for the borrowing list view
    path('borrowings/late_fee/', LatefeeListView.as_view(), name='late_fee_list'),  # Add this line for the late fee creation view
    path('borrowings/<int:pk>/pay_late_fee/', LateFeePaymentView.as_view(), name='pay_late_fee'),  # Add this line for the pay late fee view
    path('logout/', Logout.as_view(), name='logout'),  # Add this line for the logout view
]   
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

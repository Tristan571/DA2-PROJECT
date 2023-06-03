# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.db.models import Q
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.core.files import File
from django.core.paginator import Paginator
import datetime
import json
from .models import *
from .forms import *
from .cart import *

logger = logging.getLogger(__name__)

# Create your views here.
def loginPage(request):

    
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        #note: take username and password from user input
        username = request.POST.get('username')
        password = request.POST.get('password')

        #note: check if username and password exist in database
        try:
            user  = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return redirect('login')
        
        #note: check if password is correct
        user = authenticate(request, username=username, password=password)

        
    
        role = user.profile.role
        if role == '':
            messages.error(request, 'The logged in user does not have valid role.')
        else:
            
            if user is not None and role == '2':
                login(request, user)
                return redirect('librarian')
            elif user is not None and role == '3':
                login(request, user)
                return redirect('home')
            elif user is not None and role == '5':
                login(request, user)
                return redirect('clerk')
            elif user is not None and role == '4':
                login(request, user)
                return redirect('manager')
            elif user is not None and role == '1':
                login(request, user)
                return redirect('home')
                
            else:
                messages.error(request, 'Invalid username or password')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def librarian(request):
    form = BookForm()
    select = ''
    book_count = Book.objects.all().count()
    book_rental = BookRental.objects.all().count()
    book_available = book_count - book_rental

    #Chart
    # Retrieve all book rents grouped by month for the current year
    year = datetime.datetime.now().year
    rents_by_month = BookRental.objects.filter(rentDate__year=year).annotate(month=TruncMonth('rentDate')).values('month').annotate(count=Count('rentalID'))
    books_by_month = Book.objects.filter(created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(count=Count('bookID'))
    # Create a dictionary of data for all months in the current year
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    books_borrowed = [0] * 12
    for rent in rents_by_month:
        month_index = rent['month'].month - 1  # Subtract 1 to get 0-based index of month
        books_borrowed[month_index] = rent['count']

    books_added = [0] * 12
    for book in books_by_month:
        month_index = book['month'].month - 1  # Subtract 1 to get 0-based index of month
        books_added[month_index] = book['count']
    # Create a dictionary of data for the chart
    chart_data = {
        
        'labels': labels,
        'datasets': [
            {
                'label': "Books Borrowed",
                'data': books_borrowed,
                'borderColor': "#3e95cd",
                'fill': False,
            },
            {
            'label': "Books Added",
            'data': books_added,
            'borderColor': "#8e5ea2",
            'fill': False,
        },
        ],
    }

    
    # convert the chart data to a JSON string
    chart_data_json = json.dumps(chart_data)

    context = {'form': form, 'book_count': book_count, 'book_rental': book_rental,
    'select': select, 'chart_data_json': chart_data_json, 'book_available' : book_available}

    return render(request, 'base/librarian.html', context)

def clerk(request):
    form = BookForm()
    
    book_count = Book.objects.all().count()
    book_rental = BookRental.objects.all().count()
    book_available = book_count - book_rental

    #Chart
    # Retrieve all book rents grouped by month for the current year
    year = datetime.datetime.now().year
    rents_by_month = BookRental.objects.filter(rentDate__year=year).annotate(month=TruncMonth('rentDate')).values('month').annotate(count=Count('rentalID'))
    books_by_month = Book.objects.filter(created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(count=Count('bookID'))
    # Create a dictionary of data for all months in the current year
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    books_borrowed = [0] * 12
    for rent in rents_by_month:
        month_index = rent['month'].month - 1  # Subtract 1 to get 0-based index of month
        books_borrowed[month_index] = rent['count']

    books_added = [0] * 12
    for book in books_by_month:
        month_index = book['month'].month - 1  # Subtract 1 to get 0-based index of month
        books_added[month_index] = book['count']
    # Create a dictionary of data for the chart
    chart_data = {
        
        'labels': labels,
        'datasets': [
            {
                'label': "Books Borrowed",
                'data': books_borrowed,
                'borderColor': "#3e95cd",
                'fill': False,
            },
            {
            'label': "Books Added",
            'data': books_added,
            'borderColor': "#8e5ea2",
            'fill': False,
        },
        ],
    }

    
    # convert the chart data to a JSON string
    chart_data_json = json.dumps(chart_data)

    context = {'form': form, 'book_count': book_count, 'book_rental': book_rental,
     'chart_data_json': chart_data_json, 'book_available' : book_available}

    return render(request, 'base/clerk.html')

def manager(request):


    return render(request, 'base/manager.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def manageBook(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'base/manage_book.html', context)


def manageAuthor(request):
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'base/manage_author.html', context)

def registerPage(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            # user.username = user.username.lower()
            # user.save()
            form.save()
            # login(request, user)
            messages.success(request, 'Create account successfully')
            
            return redirect('login')
        else:
            messages.error(request, 'An error occurred')

    return render(request, 'base/login_register.html', {'form': form})

#note: Home view for home page
def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''

                                            #icontains is case insensitive
    bookss = Book.objects.filter( #note: This function allows you to filter the rooms based on the name of the room
        Q(topicID__name__icontains=q) | #note: we can use AND, OR to search
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) #get all rooms form Room object from modelsmodels


    
    topics = Topic.objects.all() 
    # bookss = Book.objects.all().order_by('-created')
    books = bookss.all()[:6]


    context = {'topics': topics, 'books': books}


    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def profile(request, pk):
    
    rents = BookRental.objects.filter(user=request.user)
    
    profile = Profile.objects.get(user=request.user)
    
    totalRent = BookRental.objects.filter(user=request.user).aggregate(totalRent=Sum('totalFee'))['totalRent']
    
    context = {'rents': rents, 'profile': profile, 'totalRent': totalRent}
    return render(request, 'base/profile.html', context)

def book(request, pk):

    books = Book.objects.get(id=pk)

    context = {'books': books}

    return render(request, 'base/book_component.html', context)

def cart(request):
    cart = Cart(request)
    books = cart.get_books()

    each_book_total = []
    if len(each_book_total) == None:
        for book in cart:
            price = cart.get_one_book_total_price(book)
            each_book_total.append(price)

    context = {'cart': cart, 'books': books, 'each_book_total': each_book_total}

    each_book_total.clear()

    return render(request, 'base/cart.html', context)

@require_POST
def cart_add(request):
    # book = get_object_or_404(Book, pk=pk)
    cart = Cart(request)
    book_id = request.POST['bookID']
    bookID = request.GET['txtbookID']
    print('=====>' + bookID)
    print('=====>' + request.POST['bookID'])
    book = get_object_or_404(Book, id=book_id)
    cart.add(book=book)
    data = {
        'cart_count': cart.count(),
        'success_message': f"{book.name} is added to the cart."
    }
    return JsonResponse(data)

@login_required(login_url='login')
def add_to_cart(request, pk):
    
    book = get_object_or_404(Book, pk=pk)
    cart = Cart(request)

    rent_count = BookRental.objects.filter(user=request.user, returnDate = None).count()
    if book.stock == 0:
        messages.error(request, 'This book is out of stock!')
        return redirect('search')
    elif rent_count >= 5:
        messages.error(request, 'You have already rented 5 books and they are UNRETURNED!')
        return redirect('search')
    elif cart.get_one_quantity(book) >= book.stock:  # check if user adding more books than the stock
        messages.error(request, f'The stock of {book.name} is only {book.stock}. You cannot add more books to your cart!')
        return redirect('search')
    elif cart.get_books_count() >= 5:
        messages.error(request, 'You have already added 5 books to your cart!')
        return redirect('search')
    else:
        cart.add_book(book)
        messages.success(request, "Added successfully")
        return redirect('search')

    cart_items = {'count': cart.get_books_count()}
    
    each_book_total = []
    for book in cart.get_books():
        price = 1.5 * cart.get_one_quantity(book)
        each_book_total.append(str(price)) 
    

    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    bookss = Book.objects.filter(
        Q(topicID__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    books = bookss.all()
    context = {'books': books, 'topics': topics, 'each_book_total': each_book_total}

    return render(request, 'base/search.html', context)

def add_one_book(request, pk):
    
    book = get_object_or_404(Book, pk=pk)
    cart = Cart(request)

    rent_count = BookRental.objects.filter(user=request.user, returnDate = None).count()
    if book.stock == 0:
        messages.error(request, 'This book is out of stock!')
        return redirect('oneBook', pk=pk)
    elif rent_count >= 5:
        messages.error(request, 'You have already rented 5 books and they are UNRETURNED!')
        return redirect('oneBook', pk=pk)
    elif cart.get_one_quantity(book) >= book.stock:  # check if user adding more books than the stock
        messages.error(request, f'The stock of {book.name} is only {book.stock}. You cannot add more books to your cart!')
        return redirect('oneBook', pk=pk)
    elif cart.get_books_count() >= 5:
        messages.error(request, 'You have already added 5 books to your cart!')
        return redirect('oneBook', pk=pk)
    else:
        cart.add_book(book)
        messages.success(request, "Added successfully")
        return redirect('oneBook', pk=pk)

    cart_items = {'count': cart.get_books_count()}
    
    each_book_total = []
    for book in cart.get_books():
        price = 1.5 * cart.get_one_quantity(book)
        each_book_total.append(str(price)) 
    

    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    bookss = Book.objects.filter(
        Q(topicID__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    books = bookss.all()
    context = {'book': book, 'topics': topics}

    return render(request, 'base/one_book.html', context)


def removeBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart = Cart(request)
    cart.remove_book(book)
    return redirect('cart')

@login_required(login_url='login')
def search(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    search_type = request.GET.get('search_type')

    books = []
    if q and search_type:
        if search_type == 'title':
            books = Book.objects.filter(
                Q(name__icontains=q) 
                )
        elif search_type == 'author':
            books = Book.objects.filter(
                Q(authorID__name__icontains=q) 
                )
        elif search_type == 'year':
            books = Book.objects.filter(
                Q(year__icontains=q) 
                )   
        elif search_type == 'isbn':
            books = Book.objects.filter(
                Q(bookID__icontains=q) 
                )    
    elif q:
        books = Book.objects.filter(
                Q(topicID__name__icontains=q) 
                )
    else:
        books = Book.objects.all()
    
    #Set up pagination
    p = Paginator(books, 9)
    p2 = Paginator(Book.objects.all().order_by('-created'), 9)
    page = request.GET.get('page')
    booklist = p.get_page(page)
    counts = books.count()
    booklist2 = p2.get_page(page)
    
    topics = Topic.objects.all()
    context = {'books': books, 'topics': topics, 'counts': counts, 'booklist': booklist, 'booklist2': booklist2, 'q': q, 'search_type': search_type}
    return render(request, 'base/search.html', context)


@login_required(login_url='login')
def rent(request):
    cart = Cart(request)
    books = cart.get_books()
    
    rent_count = BookRental.objects.filter(user=request.user, returnDate = None).count()
    total_will_rent = rent_count + cart.get_books_count()
    
    if rent_count >= 5:
        messages.error(request, 'You have already rented 5 books')
        return redirect('cart')
    elif total_will_rent > 5:
        messages.error(request, 'The total will rent is more than 5 books, please remove some books from your cart or RETURN some books!')
        return redirect('cart')
    else:
        for book in books:
            rent = BookRental(user = request.user, bookID = book, rentCondition = book.condition, 
                                returnCondition = None, returnDate = None, extraFee=0, totalFee = 0)
            rent.save()
            book.stock = book.stock - 1
            cart.remove_book(book)
        messages.success(request, 'Rent successfully!')
    
    return render(request, 'base/cart.html')


@login_required(login_url='login')
def oneBook(request, pk):
    book = get_object_or_404(Book, pk=pk)

    cart = Cart(request)

    rent_count = BookRental.objects.filter(user=request.user, returnDate = None).count()
    if request.method == 'POST':
        if book.stock == 0:
            messages.error(request, 'This book is out of stock!')
        if rent_count >= 5:
            messages.error(request, 'You have already rented 5 books and they are UNRETURNED!')
        else:
            cart.add_book(book)
            messages.success(request, "Added successfully")

    context = {'book': book}
    return render(request, 'base/one_book.html', context)


@login_required(login_url='login')
def addBook(request):
    form = BookForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            book = form.save(commit=False)
            book.image = request.FILES['image']
            book.save()
            form.save_m2m()
            return redirect('addBook')
        else:
            messages.error(request, 'An error occurred')
    context = {'form': form}
    return render(request, 'base/add_book.html', context)



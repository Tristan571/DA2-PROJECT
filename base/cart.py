from decimal import Decimal
from django.conf import settings
from .models import Book

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Initialize an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_book(self, book, quantity=1, update_quantity=False):
        """
        Add a book to the cart or update its quantity.
        """
        book_id = str(book.bookID)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0, 'price': str(book.price)}

        if update_quantity:
            # Update quantity to the given value
            self.cart[book_id]['quantity'] = quantity
        else:
            # Add 1 to quantity if the book is already in the cart
            if self.cart[book_id]['quantity'] < 1:
                 self.cart[book_id]['quantity'] = 1
            elif self.cart[book_id]['quantity'] < 5:
                self.cart[book_id]['quantity'] += 1

        self.save()

    def get_books(self):
        """
        Return a list of books in the cart.
        """
        books = list(Book.objects.filter(bookID__in=self.cart.keys()))
        for book in books:
            book.quantity = self.cart[str(book.bookID)]['quantity']
        return books

    def remove_book(self, book):
        book_id = str(book.bookID)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()
    def get_one_quantity(self, book):
        book_id = str(book.bookID)
        if book_id in self.cart:
            return self.cart[book_id]['quantity']
        else:
            return 0

    def get_books_count(self):
        books = list(Book.objects.filter(bookID__in=self.cart.keys()))
        sumbooks = 0
        for book in books:
            sumbooks = sumbooks + self.cart[str(book.bookID)]['quantity']
        return sumbooks
        
    def __iter__(self):
        """
        Iterate over the items in the cart and get the product objects.
        """
        book_ids = self.cart.keys()
        # Get the product objects and add them to the cart dictionary
        books = Book.objects.filter(bookID__in=book_ids)
        for book in books:
            self.cart[str(book.bookID)]['book'] = book

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(1.5 * item['quantity'])
            yield item

    def __len__(self):
        """
        Count all the items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    # def get_one_book_total_price(self, book):
    #     return 1.5 * self.cart[str(book.bookID)]['quantity']
        
        def get_one_book_total_price(self, book):
            return 1.5 * get_one_quantity(self, book)


    def get_total_price(self):
        """
        Get the total price of all items in the cart.
        """
        return sum(( 1.5 * item['quantity'] for item in self.cart.values()))

    def clear(self):
        """
        Remove all items from the cart.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        """
        Update the session data with the current contents of the cart.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView



urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('cart/', views.cart, name='cart'),
    # path('cart/add/<str:pk>', views.add_to_cart, name='addCart'),
    path('add_to_cart/<str:pk>', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:pk>/', views.removeBook, name='removeBook'),
    path('rent/', views.rent, name='rent'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('add-to-cart/<str:pk>/', views.add_one_book, name='add_one_book'),
    path('search/view/<str:pk>/', views.oneBook, name='oneBook'),
    path('librarian/', views.librarian, name='librarian'),
    path('clerk/', views.clerk, name='clerk'),
    path('manager/', views.manager, name='manager'),
    path('librarian/manage-book/', views.manageBook, name='manageBook'),
    path('librarian/manage-author/', views.manageAuthor, name='manageAuthor'),
    path('librarian/manage-book/add-book/', views.addBook, name='addBook'),
    path('cart/add/', views.cart_add, name='cart_add'),

    # path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'static/favicon/favicon.ico')),

    path('admin/', admin.site.urls),
   

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
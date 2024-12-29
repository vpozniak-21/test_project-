from django.contrib import admin
from django.urls import path
from bookreview.views import book_list, book_detail, ReviewCreateView
from django.contrib.auth import views as auth_views
from bookreview.views import index
from bookreview.views import profile
from bookreview.views import custom_logout
from bookreview.views import register
from bookreview.views import custom_login
from bookreview.views import author_detail
from bookreview.views import book_list
from bookreview.views import add_review
from bookreview.views import book_detail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('books/<int:book_id>/add_review/', add_review, name='add_review'),
    path('authors/<int:pk>/', author_detail, name='author_detail'),

]

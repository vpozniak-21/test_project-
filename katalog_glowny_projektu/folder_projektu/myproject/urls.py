from django.contrib import admin
from django.urls import path
from bookreview.views import book_list, book_detail, ReviewCreateView
from django.contrib.auth import views as auth_views
from bookreview.views import index, profile, custom_logout, register, custom_login, author_detail, book_list, add_review, book_detail, add_comprehensive_review


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
    path("add_comprehensive_review/", add_comprehensive_review, name="add_comprehensive_review"),

]

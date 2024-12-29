from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from bookreview.models import Review
from bookreview.forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

from django.shortcuts import render, get_object_or_404
from .models import Book, Review

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})


from django.shortcuts import render
from bookreview.models import Review
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'profile.html', {'reviews': reviews})

from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('login')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        # Authenticated users are redirected to the main page (index.html)
        return render(request, 'index.html')  # Render the main page for logged-in users
    else:
        # Unauthenticated users are redirected to the login page
        return redirect('login')

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user with additional details
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def custom_login(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']
        password = request.POST['password']

        user = authenticate(request, username=identifier, password=password)
        if not user:  # If not found as username, try as email
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                email_user = User.objects.get(email=identifier)
                user = authenticate(request, username=email_user.username, password=password)
            except User.DoesNotExist:
                pass
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the main page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    return render(request, 'login.html')





from django.shortcuts import render, get_object_or_404
from .models import Book, Review

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            print(f"Assigned User: {review}")  # Debugging line
            review.save()
            return redirect('book_detail', pk=book.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'book': book})

from django.shortcuts import render, get_object_or_404
from bookreview.models import Author, Book

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)
    return render(request, 'author_detail.html', {'author': author, 'books': books})


from .models import Book
from django.db.models import Q

def book_list(request):
    query = request.GET.get('q', '')  # Search query
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books, 'query': query})
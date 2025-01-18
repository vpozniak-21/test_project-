from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from bookreview.models import Review, Book, Author
from bookreview.forms import ReviewForm, CustomUserCreationForm, ComprehensiveReviewForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from bookreview.forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Avg,Q



class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})



@login_required
def profile(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'profile.html', {'reviews': reviews})


def custom_logout(request):
    logout(request)
    return redirect('login')


def index(request):
    if request.user.is_authenticated:
        # Authenticated users are redirected to the main page (index.html)
        return render(request, 'index.html')  # Render the main page for logged-in users
    else:
        # Unauthenticated users are redirected to the login page
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user with additional details
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})



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


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})


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


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)
    return render(request, 'author_detail.html', {'author': author, 'books': books})



def book_list(request):
    query = request.GET.get('q', '')  # Search query
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books = Book.objects.all()

    # Dodanie średniej oceny do każdego obiektu książki
    books = books.annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'book_list.html', {'books': books, 'query': query})


@login_required
def add_comprehensive_review(request):
    if request.method == "POST":
        form = ComprehensiveReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle existing book/author or new book/author

            # For a new author
            if form.cleaned_data["new_author_name"]:
                author = Author.objects.create(
                    name=form.cleaned_data["new_author_name"],
                    nationality=form.cleaned_data["nationality"],
                    birth_date=form.cleaned_data["birth_date"],
                )
            else:
                author = form.cleaned_data["author"]  # Use selected author

            # For a new book
            if form.cleaned_data["new_book_title"]:
                book = Book.objects.create(
                    title=form.cleaned_data["new_book_title"],
                    genre=form.cleaned_data["genre"],
                    release_date=form.cleaned_data["release_date"],
                    author=author,
                    cover_image=form.cleaned_data["cover_image"],
                )
            else:
                book = form.cleaned_data["book"]  # Use selected book

            # Create the review
            Review.objects.create(
                book=book,
                user=request.user,
                rating=form.cleaned_data["rating"],
                content=form.cleaned_data["content"],
            )
            if form.cleaned_data['cover_image']:
                book.cover_image = form.cleaned_data['cover_image']
                book.save()


            return redirect("profile")  # Redirect to profile page after saving
    else:
        form = ComprehensiveReviewForm()

    # Ensure the book is passed to the template
    book = form.cleaned_data.get("book") if form.is_valid() else None

    return render(request, "add_comprehensive_review.html", {"form": form, "book": book})

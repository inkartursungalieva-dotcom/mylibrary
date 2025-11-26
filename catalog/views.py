from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from datetime import date, timedelta
from .models import Book, Author, BookInstance, UserBookStatus
from .forms import RenewBookForm, UserBookStatusForm
from django.db.models import Q

def index(request):
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    featured_books = Book.objects.all()[:3]
    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'featured_books': featured_books,
    }
    return render(request, 'catalog/index.html', context)

class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'

    def get_queryset(self):
        queryset = Book.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(summary__icontains=query)
            ).distinct()
        return queryset

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

class AuthorListView(ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status='o'
        ).order_by('due_back')

    def post(self, request, *args, **kwargs):
        book_instance_id = request.POST.get('book_instance_id')
        book_instance = get_object_or_404(
            BookInstance,
            id=book_instance_id,
            borrower=request.user
        )

        status, created = UserBookStatus.objects.get_or_create(
            user=request.user,
            book_instance=book_instance
        )

        form = UserBookStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, f'Книга "{book_instance.book.title}" обновлена!')
        else:
            messages.error(request, 'Ошибка сохранения.')

        return HttpResponseRedirect(reverse('my-borrowed'))

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            messages.success(request, f'Книга "{book_instance.book.title}" обновлена.')
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = date.today() + timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class LoanedBooksAllListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Author, Book, BookInstance, Genre
from .forms import RenewBookForm


def index(request):
    """Домашняя страница сайта"""

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    title_word = Book.display_genre

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request, 'index.html',
        context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,
            'title_word': title_word,
            'num_visits': num_visits,
        }
    )


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'book_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book_detail'
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'author_list.html'
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'author_detail'
    template_name = 'author_detail.html'


class LoanedBooksListView(LoginRequiredMixin,
                          PermissionRequiredMixin,
                          generic.ListView
):
    model = BookInstance
    context_object_name = 'borrowed'
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 50
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status='l')


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Класс для списка взятых книг для текущего пользователя
    """

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='l').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned')
def RenewBookLibrarian(request, pk):
    """Обрабатывает обновление даты возврата у библиотекаря
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)

        if form.is_valid():

            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
        
    else:

        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
        
    return render(
        request,
        'catalog/book_renew_librarian.html',
        context = {'form': form, 'bookinst': book_inst},
    )

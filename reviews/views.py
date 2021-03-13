from django.contrib import messages
from django.shortcuts import redirect, reverse, render
from . import forms
from books.models import Book
from movies.models import Movie
from reviews.models import Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def write_review(request, pk):
    kind = request.GET.get("kind")
    if kind == "book":
        obj = Book.objects.get(pk=pk)
    else:
        obj = Movie.objects.get(pk=pk)
    form = forms.CreateReviewForm()
    return render(request, "mixins/create_review.html", {"obj": obj, "form": form, "kind":kind})


def create_review(request, pk):
    if request.method == "POST":
        kind = request.GET.get("kind")
        form = forms.CreateReviewForm(request.POST)
        if kind == "book":
            book = Book.objects.get(pk=pk)
            if not book:
                return redirect(reverse("core:home"))
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.created_by = request.user
                review.save()
                messages.success(request, "Book reviewed")
                return redirect(reverse("books:book", kwargs={"pk": book.pk}))
        elif kind == "movie":
            movie = Movie.objects.get(pk=pk)
            if not movie:
                return redirect(reverse("core:home"))
            if form.is_valid():
                review = form.save(commit=False)
                review.movie = movie
                review.created_by = request.user
                review.save()
                messages.success(request, "Movie reviewed")
                return redirect(reverse("movies:movie", kwargs={"pk": movie.pk}))


@login_required
def delete_review(request, obj_pk, review_pk):
    user = request.user
    kind = request.GET.get("kind")
    review = Review.objects.get(pk=review_pk)
    if review.created_by.pk != user.pk:
        messages.error(request, "Can't delete that review")
    else:
        review.delete()
    if kind == 'book':
        return redirect(reverse('books:book', kwargs={"pk": obj_pk}))
    else:
        return redirect(reverse('movies:movie', kwargs={"pk": obj_pk}))



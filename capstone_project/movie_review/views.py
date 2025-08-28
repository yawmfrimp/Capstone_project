from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Movie, Review
from django.views.generic import DetailView, CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializer import MovieSerializer
from django.forms import modelform_factory
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test




# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_member(user):
     return user.is_authenticated and user.role == 'member'

'''An 'Admin' view that only users with the 'Admin' role can access.'''
@login_required
@user_passes_test(is_admin, login_url='login', redirect_field_name=None)
def admin_view(request):
    return render(request, 'movie_review/admin_view.html')

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'movie_review/register.html'

class MovieDetailAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'title'

def list_movies(request):
    """This fucntion list all movies available"""
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, 'movie_review/list_movies.html', context)
    

def list_reviews(request, title):
    '''this function list reviews for a specific movie'''
    movie = get_object_or_404(Movie, title=title)
    reviews = get_list_or_404(Review, movie_title=title)
    context = {'review_list': reviews, 'movie': movie}
    return render(request,'movie_review/list_reviews.html', context)


@login_required
@permission_required('movie_review.delete_movie', raise_exception=True)
def delete_movie(request,title):
    """This function allows the admin to delete a movie by title"""
    movie = get_object_or_404(Movie, title=title)
    if request.method == 'POST':
        movie.delete()
        messages.success(request,f'"{movie.title}" was deleted.')
        return redirect('list_movies')
    return render(request, 'movie_review/movie_confirm_delete.html', {'movie': movie})

MovieForm = modelform_factory(Movie, fields=['title', 'director'])

@login_required
@permission_required('movie_review.change_movie', raise_exception=True)
def edit_movie(request,title):
    '''This function allows the admin to edit the properties of a movie by title'''
    movie = get_object_or_404(Movie, title=title)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('list_movies')
    else:
        form = MovieForm(instance=movie)
    
    return render(request, 'relationship_app/movie_form.html', {
        'form' : form,
        'edit' : True,
        'movie' : movie,
    })

@login_required
@permission_required('movie_review.add_movie', raise_exception=True)
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_movie')
        else:
            form = MovieForm()
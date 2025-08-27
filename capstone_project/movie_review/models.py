from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

'''model for movie'''
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=200)
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    trailer_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} released on {self.release_date}'

'''model for user'''
class User(AbstractUser):
    joined_date = models.DateField(default=date.today)

    def __str__(self):
        return self.username

'''model for reviews'''
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    RATING_CHOICES = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    ]
    rating = models.SmallIntegerField(choices=RATING_CHOICES, default=1, help_text='Rating of the movie where 1 is the lowest and 5 is the highest')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['movie', 'user'], name='unique_review_per_user_per_movie')
        ]

    def __str__(self):
        return f'{self.user} rated {self.movie}, {self.rating}'
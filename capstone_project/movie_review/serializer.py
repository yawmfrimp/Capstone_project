from rest_framework import serializers
from .models import Movie, Review
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'

    def get_average_rating(self, obj):
        # Get the average for all the ratings of this particular movie
        avg = obj.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if avg is not None:
            return round(avg,1)
        else:
            None
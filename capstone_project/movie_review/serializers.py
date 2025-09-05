from rest_framework import serializers
from .models import Movie, Review, User
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    '''This serializer retrieves a review for the movie while showing the creator of the review as well as the movie reviewed'''
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), write_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class MovieDetailSerializer(serializers.ModelSerializer):
    '''This serializer retrieves the details for a movie showing all the reviews and the average rating for the movie'''
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = '__all__'

    def get_average_rating(self, obj):
        # Get the average for all the ratings of this particular movie
        avg = obj.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if avg is not None:
            return round(avg,1)
        else:
            return None

class MovieSerializer(serializers.ModelSerializer):
    '''This serializer shows a list of all the movies with their average ratings'''
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = '__all__'

    def get_average_rating(self, obj):
         # Get the average for all the ratings of this particular movie
        avg = obj.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if avg is not None:
            return round(avg,1)
        else:
            return None


class UserSerializer(serializers.ModelSerializer):
    '''This serializer shows the details of a user and is for admin use only'''
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'joined_date']
        read_only_fields = ['id', 'joined_date']

class RegisterSerializer(serializers.ModelSerializer):
    '''This serializer handles the registeration of new users'''
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','email', 'password']
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role='member'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
from django.shortcuts import get_object_or_404
from .models import Movie, Review, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions, generics, status
from .serializers import MovieSerializer, MovieDetailSerializer, ReviewSerializer, RegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class IsMember(permissions.BasePermission):
    '''Allows only authenticated users with role='member' to create reviews.'''
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'member'
        )

class IsReviewOwnerAndMember(permissions.BasePermission):
    '''Allows only the member who created the review to update it.'''
    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'member'
            and obj.user == request.user
        )
    
class IsAdminOrReviewOwner(permissions.BasePermission):
    '''Allows deletion of review by admins or by the owner of review.'''
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        # fallback to member owner
        return obj.user == request.user
    

class IsAdminUserRole(permissions.BasePermission):
    '''Allows access only to users with role='admin' '''
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer   # your serializer
    # permission_classes, queryset etc.

    def create(self, request, *args, **kwargs):
        # 1. Let DRF run validation & save the user
        resp = super().create(request, *args, **kwargs)

        # 2. Grab the next URL, if any
        next_url = request.query_params.get('next')
        if next_url:
            # 3. Change status to a redirect and set Location
            resp.status_code = status.HTTP_303_SEE_OTHER
            resp['Location'] = next_url

        return resp


class LoginAPIView(APIView):
    '''This view handles User Login'''
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class MovieListCreateAPIView(generics.ListCreateAPIView):
    '''This view lists all the movies available or creates a new movie (only admins)'''
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        '''This function checks whether the user is an admin or memeber depending on the request method'''
        if self.request.method == 'POST':
            return [IsAdminUserRole()]
        else:
            return [permissions.AllowAny()]
        
class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''This view retrieves details of a particular movie, and also allows for updating or deleting movies (admin only)'''
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    lookup_field = 'title'

    def get_permissions(self):
        '''This function checks whether a user is admin or member depending on the request method'''
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUserRole()]
        else:
            return [permissions.AllowAny()]
        
class ReviewListCreateAPIView(generics.ListCreateAPIView):
    '''This view lists reviews for a movie or lets a member create a review '''
    serializer_class = ReviewSerializer

    def get_queryset(self):
        '''This function gets the reviews for a movie using the title as a look up'''
        movie = get_object_or_404(Movie, title=self.kwargs['title'])
        return Review.objects.filter(movie=movie)

    def get_permissions(self):
        '''This function checks for whether a user is a member if they are creating a review'''
        if self.request.method == 'POST':
            return [IsMember()]
        return [AllowAny()]

    def perform_create(self, serializer):
        '''This function creates a new review for a movie using the title as a look up'''
        movie = get_object_or_404(Movie, title=self.kwargs['title'])
        serializer.save(user=self.request.user, movie=movie)

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''This view retrieves reviews for a movie, updates or delete a review (review owner or admin)'''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        '''This function checks for the permissions of a user depending on the request method'''
        if self.request.method in ['PUT', 'PATCH']:
            return [IsReviewOwnerAndMember()]
        if self.request.method == 'DELETE':
            return [IsAdminOrReviewOwner()]
        return [AllowAny()]
        
class AdminCreateUserAPIView(generics.CreateAPIView):
    '''This view is to create a new admin (admin only)'''
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUserRole]

    def perform_create(self, serializer):
        serializer.save(role='admin')

        


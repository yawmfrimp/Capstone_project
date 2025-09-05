from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Movie, Review


# Create your tests here.
User = get_user_model()


class ReviewPermissionsTestCase(APITestCase):
    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass", role="admin"
        )
        self.member_user = User.objects.create_user(
            username="member", password="memberpass", role="member"
        )
        self.other_member = User.objects.create_user(
            username="other", password="otherpass", role="member"
        )

        # Create tokens
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.member_token = Token.objects.create(user=self.member_user)
        self.other_member_token = Token.objects.create(user=self.other_member)

        # Create a movie (adjust required fields as per your Movie model)
        self.movie = Movie.objects.create(
            title="testmovie",
            # e.g. description="A test movie",
            # release_date="2025-01-01",
            # … any other non-nullable fields …
        )

        # Create an initial review by the member_user
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.member_user,
            rating=5,
            comment="Outstanding!"
        )

    def test_list_reviews_anonymous(self):
        """
        GET /api/movies/{title}/reviews/ should be open to everyone.
        """
        url = reverse("review-list", kwargs={"title": self.movie.title})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_review_unauthenticated_forbidden(self):
        """
        Anonymous POST to /api/movies/{title}/reviews/ should be 401 UNAUTHORIZED
        (no token sent).
        """
        url = reverse("review-list", kwargs={"title": self.movie.title})
        payload = {
            "rating": 4,
            "comment": "Nice flick",
            "movie": self.movie.id
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_admin_forbidden(self):
        """
        Only members can create reviews; admins should get 403.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        url = reverse("review-list", kwargs={"title": self.movie.title})
        payload = {"rating": 3, "comment": "Okay", "movie": self.movie.id}
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_review_member_success(self):
        """
        A *new* member (other_member) can post a review for this movie.
        """
        # switch to other_member’s token
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.other_member_token.key}"
        )

        url = reverse("review-list", kwargs={"title": self.movie.title})
        payload = {
            "rating": 4,
            "comment": "Really enjoyed it",
            "movie": self.movie.id
        }

        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", res.data)
        self.assertEqual(res.data["comment"], "Really enjoyed it")

    
    def test_duplicate_review_same_user_forbidden(self):
        """
        A member cannot post more than one review for the same movie.
        Should return 400 BAD REQUEST.
        """
        # Authenticate as the same member who already reviewed in setUp
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.member_token.key}")

        url = reverse("review-list", kwargs={"title": self.movie.title})
        payload = {
            "rating": 4,
            "comment": "Trying to review again",
            "movie": self.movie.id
        }

        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", res.data)


    def test_retrieve_review_public(self):
        """
        GET /api/reviews/{pk}/ is public.
        """
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_review_owner_success(self):
        """
        The member who created the review can PATCH their own review.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.member_token.key}")
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        res = self.client.patch(url, {"comment": "Updated comment"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, "Updated comment")

    def test_update_review_admin_forbidden(self):
        """
        Admins are not allowed to update reviews.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        res = self.client.patch(url, {"comment": "Admin edit"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_review_other_member_forbidden(self):
        """
        A different member cannot update someone else's review.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.other_member_token.key}"
        )
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        res = self.client.patch(url, {"comment": "Not mine"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_owner_success(self):
        """
        A member may delete their own review (204 NO CONTENT).
        """
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.member_token.key}"
        )
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

    def test_delete_review_admin_success(self):
        """
        Only admins can delete a review.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

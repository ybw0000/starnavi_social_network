from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from posts.models import Like
from posts.models import Post
from user.models import User


class PostsTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def test__list_posts__success(self):
        user = User.objects.create_user(username='username', password='password')
        post = Post.objects.create(text='test post', author=user)

        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}

        url = reverse('create-list-post')
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertListEqual([{'text': 'test post', 'author': user.id, 'id': post.id}], response.json())

    def test__create_post__success(self):
        User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}

        request_data = {'text': 'test post'}

        url = reverse('create-list-post')
        with self.assertNumQueries(3):
            response = self.client.post(path=url, data=request_data, headers=headers)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn('author', response.json())
        self.assertIn('text', response.json())

    def test__retrieve_post__success(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test post', author=user)

        url = reverse('retrieve-post', args=[post.id])
        with self.assertNumQueries(3):
            response = self.client.get(path=url, headers=headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({'text': 'test post', 'author': user.id, 'id': post.id}, response.json())

    def test__like_post__success__like(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test post', author=user)

        url = reverse('like-post', args=[post.id])
        with self.assertNumQueries(5):
            response = self.client.patch(path=url, headers=headers)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertDictEqual({'message': 'Liked.'}, response.json())
        self.assertNotEqual(Like.objects.first(), None)

    def test__like_post__success__unlike(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test post', author=user)
        Like.objects.create(post=post, user=user)

        url = reverse('like-post', args=[post.id])
        with self.assertNumQueries(5):
            response = self.client.patch(path=url, headers=headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({'message': 'Unliked.'}, response.json())
        self.assertEqual(Like.objects.first(), None)

    def test__like_post__fail__post_not_found(self):
        User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}

        url = reverse('like-post', args=[1])
        with self.assertNumQueries(3):
            response = self.client.patch(path=url, headers=headers)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertDictEqual({'detail': 'Not found.'}, response.json())

    def test__analytics__success(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test', author=user)
        Like.objects.create(post=post, user=user)

        url = reverse('analytics')
        with self.assertNumQueries(3):
            response = self.client.get(path=url, headers=headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual([], response.json())

    def test__analytics__success__with_date_from_case1(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test', author=user)
        like = Like.objects.create(post=post, user=user)
        params = {'date_from': like.created_at.strftime('%Y-%m-%d')}

        url = reverse('analytics')
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
                data=params,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual([], response.json())

    def test__analytics__success__with_date_from_case2(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test', author=user)
        like = Like.objects.create(post=post, user=user)
        params = {'date_from': (like.created_at + timedelta(days=1)).strftime('%Y-%m-%d')}

        url = reverse('analytics')
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
                data=params,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertListEqual([], response.json())

    def test__analytics__success__with_date_to_case1(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test', author=user)
        like = Like.objects.create(post=post, user=user)
        params = {'date_to': like.created_at.strftime('%Y-%m-%d')}

        url = reverse('analytics')
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
                data=params,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertListEqual([], response.json())

    def test__analytics__success__with_date_to_case2(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test', author=user)
        like = Like.objects.create(post=post, user=user)
        params = {'date_to': (like.created_at + timedelta(days=1)).strftime('%Y-%m-%d')}

        url = reverse('analytics')
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
                data=params,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual([], response.json())

    def test__analytics__success__with_date_from_and_date_to_case1(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test', author=user)
        like = Like.objects.create(post=post, user=user)
        params = {
            'date_to': like.created_at.strftime('%Y-%m-%d'),
            'date_from': like.created_at.strftime('%Y-%m-%d'),
        }

        url = reverse('analytics')
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
                data=params,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual([], response.json())

    def test__analytics__success__with_date_from_and_date_to_case2(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}
        post = Post.objects.create(text='test', author=user)
        like = Like.objects.create(post=post, user=user)
        params = {
            'date_to': (like.created_at - timedelta(days=1)).strftime('%Y-%m-%d'),
            'date_from': (like.created_at + timedelta(days=1)).strftime('%Y-%m-%d'),
        }
        like.created_at = like.created_at - timedelta(days=2)
        like.save(update_fields=['created_at'])

        url = reverse('analytics')
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
                data=params,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual([], response.json())

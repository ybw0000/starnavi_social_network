from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User


class AuthTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def test__signup__success(self):
        request_data = {
            'username': 'username',
            'password': 'password',
        }

        url = reverse('signup')
        with self.assertNumQueries(3):
            response = self.client.post(
                path=url,
                data=request_data,
            )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

    def test__signup__fail__user_already_exist(self):
        request_data = {
            'username': 'username',
            'password': 'password',
        }
        User.objects.create_user(username=request_data['username'], password=request_data['password'])

        url = reverse('signup')
        with self.assertNumQueries(1):
            response = self.client.post(
                path=url,
                data=request_data,
            )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual({'username': ['A user with that username already exists.']}, response.json())

    def test__signin__success(self):
        request_data = {
            'username': 'username',
            'password': 'password',
        }
        User.objects.create_user(username=request_data['username'], password=request_data['password'])

        url = reverse('signin')
        with self.assertNumQueries(2):
            response = self.client.post(
                path=url,
                data=request_data,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

    def test__signin__fail(self):
        request_data = {
            'username': 'username',
            'password': 'password',
        }

        url = reverse('signin')
        with self.assertNumQueries(1):
            response = self.client.post(
                path=url,
                data=request_data,
            )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertDictEqual({'detail': 'No active account found with the given credentials'}, response.json())

    def test__activity__success(self):
        user = User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}

        url = reverse('user-activity', args=[user.username])
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
            )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('last_login', response.json())
        self.assertIn('last_request', response.json())

    def test__activity__fail__not_found(self):
        User.objects.create_user(username='username', password='password')
        token = TokenObtainPairSerializer(data={'username': 'username', 'password': 'password'})
        token.is_valid(raise_exception=False)
        headers = {'Authorization': 'Bearer ' + token.validated_data['access']}

        url = reverse('user-activity', args=['not-exist'])
        with self.assertNumQueries(3):
            response = self.client.get(
                path=url,
                headers=headers,
            )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertDictEqual({'detail': 'Not found.'}, response.json())

    def test__activity__fail__unauthorized(self):
        url = reverse('user-activity', args=['not-exist'])
        with self.assertNumQueries(0):
            response = self.client.get(path=url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertDictEqual({'detail': 'Authentication credentials were not provided.'}, response.json())

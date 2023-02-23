from django.test import TestCase
from ..views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView
from ..models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..serializers import UserRegistrationSerializer, UserLoginSerializer


class UserRegistrationAPIViewTestCase(TestCase):
    """
        Тесты для UserRegistrationAPIView
    """
    def setUp(self) -> None:
        self.view_class = UserRegistrationAPIView

    def test_permissions_classes(self):
        cur_perms = self.view_class.permission_classes
        expected_perms = (AllowAny,)
        self.assertEqual(cur_perms, expected_perms)

    def test_serializer_class(self):
        cur_serializer = self.view_class.serializer_class
        expected_serializer = UserRegistrationSerializer
        self.assertEqual(cur_serializer, expected_serializer)

    def test_http_method_names(self):
        cur_methods = self.view_class.http_method_names
        expected_methods = ('post',)
        self.assertEqual(cur_methods, expected_methods)

    def test_registration(self):
        endpoint_url = '/users/register/'
        registration_data = dict(
            username='test_reg',
            password='test_reg',
            email='test_reg@mail.ru',
            first_name='test_reg',
            last_name='test_reg',
            birthday='2023-02-23'
        )
        resp = self.client.post(endpoint_url, data=registration_data, follow=True)
        self.assertEqual(resp.status_code, 201)
        resp_data = resp.data
        expected_resp_user_data = [
            'id', 'username', 'email', 'first_name', 'last_name', 'birthday', 'created_at', 'tokens'
        ]
        self.assertEqual(list(resp_data.keys()), expected_resp_user_data)
        expected_resp_tokens_data = ['refresh', 'access']
        self.assertEqual(list(resp_data['tokens'].keys()), expected_resp_tokens_data)
        new_user = User.objects.filter(username='test_reg')
        self.assertTrue(new_user.exists())


class UserLoginAPIViewTestCase(TestCase):
    """
        Тесты для UserLoginAPIView
    """
    @classmethod
    def setUpTestData(cls):
        extra_kwargs = dict(
            email='test_login@mail.ru',
            first_name='test_login',
            last_name='test_login',
            birthday='2023-02-23'
        )
        User.objects.create_user(username='test_login', password='test_login', **extra_kwargs)

    def setUp(self) -> None:
        self.view_class = UserLoginAPIView

    def test_permissions_classes(self):
        cur_perms = self.view_class.permission_classes
        expected_perms = (AllowAny,)
        self.assertEqual(cur_perms, expected_perms)

    def test_serializer_class(self):
        cur_serializer = self.view_class.serializer_class
        expected_serializer = UserLoginSerializer
        self.assertEqual(cur_serializer, expected_serializer)

    def test_http_method_names(self):
        cur_methods = self.view_class.http_method_names
        expected_methods = ('post',)
        self.assertEqual(cur_methods, expected_methods)

    def test_login(self):
        endpoint_url = '/users/login/'
        login_data = dict(
            username='test_login',
            password='test_login',
        )
        resp = self.client.post(endpoint_url, data=login_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        resp_data = resp.data
        expected_resp_user_data = [
            'id', 'username', 'first_name', 'last_name', 'birthday', 'tokens'
        ]
        self.assertEqual(list(resp_data.keys()), expected_resp_user_data)
        expected_resp_tokens_data = ['refresh', 'access']
        self.assertEqual(list(resp_data['tokens'].keys()), expected_resp_tokens_data)


class UserLogoutAPIViewTestCase(TestCase):
    """
        Тесты для UserLogoutAPIView
    """
    @classmethod
    def setUpTestData(cls):
        extra_kwargs = dict(
            email='test_logout@mail.ru',
            first_name='test_logout',
            last_name='test_logout',
            birthday='2023-02-23'
        )
        User.objects.create_user(username='test_logout', password='test_logout', **extra_kwargs)

    def setUp(self) -> None:
        self.view_class = UserLogoutAPIView

    def test_permissions_classes(self):
        cur_perms = self.view_class.permission_classes
        expected_perms = (IsAuthenticated,)
        self.assertEqual(cur_perms, expected_perms)

    def test_http_method_names(self):
        cur_methods = self.view_class.http_method_names
        expected_methods = ('post',)
        self.assertEqual(cur_methods, expected_methods)

    def test_logout_if_not_refresh(self):
        endpoint_url = '/users/logout/'
        logout_data = dict(refresh='')
        resp = self.client.post(endpoint_url, data=logout_data, follow=True)
        self.assertEqual(resp.status_code, 401)

    def test_logout(self):
        login_endpoint_url = '/users/login/'
        login_data = dict(username='test_logout', password='test_logout')
        resp = self.client.post(login_endpoint_url, data=login_data, follow=True)
        tokens = resp.data.get('tokens')

        logout_endpoint_url = '/users/logout/'
        logout_data = dict(refresh=tokens.get('refresh'))
        resp = self.client.post(
            logout_endpoint_url,
            data=logout_data,
            follow=True,
            HTTP_AUTHORIZATION=f'Token {tokens.get("access")}'
        )
        self.assertEqual(resp.status_code, 205)
        resp = self.client.post(
            logout_endpoint_url,
            data=logout_data,
            follow=True,
            HTTP_AUTHORIZATION=f'Token {tokens.get("access")}'
        )
        self.assertEqual(resp.status_code, 400)

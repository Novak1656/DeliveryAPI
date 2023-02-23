from django.test import TestCase
from rest_framework.serializers import ReadOnlyField, CharField

from ..serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from ..models import User


class UserSerializerTestCase(TestCase):
    """
        Тесты для сериализатора пользователей
    """
    def setUp(self) -> None:
        self.serializer_class = UserSerializer

    def test_model(self):
        cur_model = self.serializer_class.Meta.model
        expected_model = User
        self.assertEqual(cur_model, expected_model)

    def test_fields(self):
        cur_fields = self.serializer_class.Meta.fields
        expected_fields = ('id', 'username', 'first_name', 'last_name', 'birthday')
        self.assertEqual(cur_fields, expected_fields)


class UserRegistrationSerializerTestCase(TestCase):
    """
        Тесты для сериализатора регистрации пользователей
    """
    def setUp(self) -> None:
        self.serializer_class = UserRegistrationSerializer
        self.serializer = UserRegistrationSerializer()

    def test_model(self):
        cur_model = self.serializer_class.Meta.model
        expected_model = User
        self.assertEqual(cur_model, expected_model)

    def test_fields(self):
        cur_fields = self.serializer_class.Meta.fields
        expected_fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'birthday', 'created_at')
        self.assertEqual(cur_fields, expected_fields)

    def test_extra_kwargs(self):
        cur_extra_kwargs = self.serializer_class.Meta.extra_kwargs
        expected_extra_kwargs = {'password': {'write_only': True}}
        self.assertEqual(cur_extra_kwargs, expected_extra_kwargs)

    def test_custom_fields(self):
        field_class = self.serializer.fields['created_at'].__class__
        expected_field_class = ReadOnlyField
        self.assertEqual(field_class, expected_field_class)

    def test_create(self):
        data = dict(
            username='test_reg_ser',
            password='test_reg_ser',
            email='test_reg_ser@mail.ru',
            first_name='test_reg_ser',
            last_name='test_reg_ser',
            birthday='2023-02-23'
        )
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cur_data = list(serializer.data.keys())
        expected_data = ['id', 'username', 'email', 'first_name', 'last_name', 'birthday', 'created_at']
        self.assertEqual(cur_data, expected_data)
        user = User.objects.filter(username='test_reg_ser')
        self.assertTrue(user.exists())


class UserLoginSerializerTestCase(TestCase):
    """
        Тесты для сериализатора авторизации пользователей
    """
    @classmethod
    def setUpTestData(cls):
        extra_kwargs = dict(
            email='test_login_ser@mail.ru',
            first_name='test_login_ser',
            last_name='test_login_ser',
            birthday='2023-02-23'
        )
        User.objects.create_user(username='test_login_ser', password='test_login_ser', **extra_kwargs)

    def setUp(self) -> None:
        self.serializer_class = UserLoginSerializer
        self.serializer = UserLoginSerializer()

    def test_fields(self):
        cur_fields = tuple(self.serializer.fields.keys())
        expected_fields = ('username', 'password')
        self.assertEqual(cur_fields, expected_fields)

    def test_fields_classes(self):
        cur_fields_classes = {field: field_class.__class__ for field, field_class in self.serializer.fields.items()}
        expected_fields_classes = dict(username=CharField, password=CharField)
        self.assertEqual(cur_fields_classes, expected_fields_classes)

    def test_validate_if_valid(self):
        data = dict(username='test_login_ser', password='test_login_ser')
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        cur_user = serializer.validated_data
        expected_user = User.objects.get(username='test_login_ser')
        self.assertEqual(cur_user, expected_user)
        self.assertTrue(cur_user.is_authenticated)

    def test_validate_if_invalid(self):
        data = dict(username='dawdawfw', password='daegrgr')
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        cur_errors = [error for error in serializer.errors.get('non_field_errors')]
        expected_errors = ['Неверный логин или пароль']
        self.assertEqual(cur_errors, expected_errors)

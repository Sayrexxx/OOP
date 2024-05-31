from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import UserCreationForm
from .models.user import MyUser

class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password': 'complexpassword123',
            'email': 'testuser@example.com',
            'phone_number': '+375291234567',
            'age': 30,
            'role': 'passenger',
        }
        self.user = MyUser.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            email=self.user_data['email'],
            phone_number=self.user_data['phone_number'],
            age=self.user_data['age'],
            role=self.user_data['role'],

        )
        self.client.login(username='testuser', password='complexpassword123')
        self.profile_url = reverse('profile')

    def test_profile_view_contains_edit_button_for_authenticated_user(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')


class RegisterPassengerViewTest(TestCase):

    def test_register_passenger_view_get(self):
        response = self.client.get(reverse('register_passenger'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_register_passenger_view_post_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '+375291234567',
            'age': 25,
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('register_passenger'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        User = get_user_model()
        user = MyUser.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '+375291234567')
        self.assertEqual(user.age, 25)
        self.assertEqual(user.role, 'passenger')

    def test_register_passenger_view_post_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '12345',
            'age': 25,
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('register_passenger'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)
        self.assertIn('phone_number', response.context['form'].errors)

from .models.user import MyUser
from .models.booking import Booking

from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

import re
import logging


logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s')


phone_number_pattern = re.compile(r'\+375(25|29|33|44)\d{7}')

class PassengerCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=13, required=True)
    age = forms.IntegerField(min_value=18, required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'phone_number', 'age', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number_pattern.match(phone_number):
            raise forms.ValidationError("Неверный формат номера телефона. Пожалуйста, введите номер в формате +375(25|29|33)XXXXXXX.")
        return phone_number

    def save(self, commit=True):
        user = super(PassengerCreationForm, self).save(commit=False)
        user.role = 'passenger'
        if commit:
            user.save()
        return user
    
    
class AdministratorCreationForm(UserCreationForm):
    secret_key = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('secret_key', 'username', 'email', 'phone_number', 'age', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        check_secret_key = self.cleaned_data['secret_key']
        if not phone_number_pattern.match(phone_number):
            raise forms.ValidationError("Неверный формат номера телефона. Пожалуйста, введите номер в формате +375(25|29|33)XXXXXXX.")
        if not check_secret_key == settings.SECRET_KEY_FOR_USER:
            raise forms.ValidationError("Неверный secret key. Пожалуйста обратитесь к\n"
                                        "администрации для получения валидного ключа")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'administrator'
        logging.info(user.__dict__)
            
        if commit:
            user.save()
            
        return user



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class BookingForm(ModelForm):    
    
    class Meta:
        model = Booking
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': 1}),  
        }

    def __init__(self, *args, **kwargs):
        self.available_seats = kwargs.pop('available_seats', None)  
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        logging.info(f"Amount: {amount}")  
        if self.available_seats == 0:
            raise ValidationError(f"По данному перелёту не осталось свободных мест")
        if amount > self.available_seats:
            raise ValidationError(f"Выберите количество мест, не превосходящее {self.available_seats}.")
        if amount == 0:
            raise ValidationError(f"Выберите количество мест, большее нуля")
        return amount


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone_number', 'age']
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number_pattern.match(phone_number):
            raise forms.ValidationError("Неверный формат номера телефона. Пожалуйста, введите номер в формате +375(25|29|33|44)XXXXXXX.")
        return phone_number
    

class SearchByCityForm(forms.Form):
    city = forms.CharField(max_length=100, label='Airport',
                           widget=forms.TextInput(attrs={'placeholder': 'Enter airport name'}))
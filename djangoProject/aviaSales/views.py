from .models.user import MyUser
from .models.flight import Flight
from .models.booking import Booking

from .forms import *

from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
import logging

logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s')


def getUserRole(name):
    if name != None:
        user = MyUser.objects.all().filter(username=name).first()
        if user != None:
            role = MyUser.objects.all().filter(username=name).first().role
            return role


def register_passenger(request):
    if request.method == 'POST':
        form = PassengerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticate(request)
            login(request, user)
            return redirect('home')
    else:
        form = PassengerCreationForm()
    return render(request, 'register.html', {'form': form})


def register_administrator(request):
    if request.method == 'POST':
        form = AdministratorCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            authenticate(request)
            login(request, user)
            return redirect('home')
    else:
        form = AdministratorCreationForm()
    return render(request, 'register.html', {'form': form})


class BaseViewContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['title'] = kwargs.get('title', 'Default Title')
        return context


class LoginUser(BaseViewContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


def profile_view(request):
    name = request.user.username
    user = get_object_or_404(MyUser, id=request.user.id)
    context = {
        'status': getUserRole(name),
        'email': user.email,
        'age': user.age,
        'phone_number': user.phone_number,
        'username': user.username,
        'edit_url': reverse('edit_profile'),
    }
    logging.info(f'Profile: {name}')
    return render(request, 'profile.html', context)

def edit_profile_view(request):
    user = request.user
    if not isinstance(user, MyUser):
        user = MyUser.objects.get(username=request.user.username)

    form_class = UserProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = form_class(instance=user)
    return render(request, 'edit_profile.html', {'form': form})


class FlightListView(ListView):
    model = Flight

    def get(self, request, *args, **kwargs):
        flights = Flight.objects.all()
        name = request.user.username

        context = {
            'flights': flights,
            'getUserRole': getUserRole(name),
        }
        return render(request, 'flights.html', context)

   

class BookingCreateView(View):
    warning_message_text = ""

    def get(self, request, current_flight_id, *args, **kwargs):
        warning_message_text = ""
        if request.user.is_authenticated and getUserRole(request.user.username) == 'passenger' and \
                Flight.objects.filter(id=current_flight_id).exists():
            flight = Flight.objects.get(id=current_flight_id)

            form = BookingForm(available_seats=flight.available_seats)
            context = {
                'flight': flight,
                'form': form,
            }
            return render(request, 'booking_form.html', context)
        else:
            warning_message_text = 'Пожалуйста, авторизуйтесь, чтобы оформить заказ'
        logging.warning(f'UserBookingListView: {warning_message_text}')
        return render(request, 'warning_message.html', {'warning_message_text': warning_message_text})

    def post(self, request, current_flight_id, *args, **kwargs):
        warning_message_text = ""
        if request.user.is_authenticated and getUserRole(request.user.username) == 'passenger' and \
                Flight.objects.filter(id=current_flight_id).exists():
            flight = Flight.objects.get(id=current_flight_id)
            form = BookingForm(request.POST, available_seats=flight.available_seats)

            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= flight.available_seats:
                    Booking.objects.create(
                        user=MyUser.objects.get(username=request.user.username),
                        flight=flight,
                        amount=amount,
                        price=amount * flight.price,
                    )
                    flight.available_seats -= amount
                    flight.save()
                    logging.info('created Booking object')
                    return redirect('home')
                else:
                    warning_message_text = 'Недостаточно свободных мест'
            else:
                warning_message_text = form.errors
        else:
            warning_message_text = 'Пожалуйста, авторизуйтесь, чтобы оформить заказ'
        logging.warning(f'UserBookingListView: {warning_message_text}')
        return render(request, 'warning_message.html', {'warning_message_text': warning_message_text})


class UserBookingListView(View):
    def get(self, request):
        warning_message_text = ""
        if request.user.is_authenticated :
            if not request.user.is_superuser:

                current_user = MyUser.objects.get(username=request.user.username)

                if getUserRole(request.user.username) == 'passenger':
                    user_bookings = Booking.objects.all().filter(user=current_user)

                    if user_bookings:
                        bookings_data = []
                        for booking in user_bookings:
                            bookings_data.append({
                                "number": booking.number,
                                "price": booking.price,
                                "status": booking.status,
                            })
                            logging.info(f"booking NUMBER: {booking.number}")
                        context = {
                            'bookings': bookings_data,
                            'getUserRole': getUserRole(current_user.username),
                        }
                        logging.info(f"bookings: {bookings_data}")

                        logging.info("UserBookingListView: passenger booking list was successfully created")
                        return render(request, 'bookings.html', context=context)
                    else:
                        warning_message_text = 'Отсутствуют брони, перейдите в каталог перелётов и найдите для себя что-нибудь интересное'
                else:
                    user_bookings = Booking.objects.all()
                    logging.info(f"123: {user_bookings.first()}")
                    if user_bookings:
                        bookings_data = []
                        for booking in user_bookings:
                            bookings_data.append({
                                "number": booking.number,
                                "passenger": booking.user,
                                "amount": booking.amount,
                                "price": booking.price,
                                "date_created": booking.date_created,
                                "status": booking.status
                            })
                            logging.info(f"booking NUMBER: {booking.number}")
                        context = {
                            'bookings': bookings_data,
                            'getUserRole': getUserRole(current_user.username),
                            'STATUS_CHOICES': booking.STATUS_CHOICES
                        }
                        logging.info(f"bookings: {bookings_data}")
                        logging.info("UserbookingListView: employee booking list was successfully created")
                        return render(request, 'bookings.html', context=context)
                    else:
                        warning_message_text = 'Для ваших товаров не найдено ни одного заказа'
        else:
            warning_message_text = 'Пожалуйста, авторизуйтесь для получения списка ваших заказов'
        logging.warning(f'UserbookingListView: {warning_message_text}')
        return render(request, 'warning_message.html', {'warning_message_text': warning_message_text})


def cancel_booking(request, number):
    booking = get_object_or_404(Booking, number=number)
    flight = booking.flight
    if request.method == 'POST':
        booking.status = "Отменён"
        booking.save()
        flight.available_seats += booking.amount
        flight.save()
    return redirect('user_bookings')



def edit_booking_status(request, number):
    booking = get_object_or_404(Booking, number=number)
    if request.method == 'POST':
        selected_status = request.POST.get('status')
        if selected_status in dict(booking.STATUS_CHOICES).keys():
            booking.status = selected_status
            booking.save()
            return redirect('user_bookings')
        else:
            return HttpResponseForbidden("Неверный статус")
    return render(request, 'news.html')

def delete_booking(request, number):
    booking = get_object_or_404(Booking, number=number)
    flight = booking.flight
    if request.method == 'POST':
        flight.available_seats += booking.amount
        flight.save()
        booking.delete()
    return redirect('all_bookings')

def get_all_bookings(request):
    user_bookings = Booking.objects.all()
    if user_bookings:
        bookings_data = []
        for booking in user_bookings:
            bookings_data.append({
                "number": booking.number,
                "passenger": booking.user,
                "amount": booking.amount,
                "price": booking.price,
                "date_created": booking.date_created,
                "status": booking.status
            })
            logging.info(f"booking NUMBER: {booking.number}")
        context = {
            'bookings': bookings_data,
            'getUserRole': getUserRole(request.user.username),
            'STATUS_CHOICES': booking.STATUS_CHOICES
        }
        logging.info(f"bookingS: {bookings_data}")
        return render(request, 'bookings.html', context=context)
    else:
        warning_message_text = 'На сервере отсутствуют активные брони'
    return render(request, 'warning_message.html', {'warning_message_text': warning_message_text})
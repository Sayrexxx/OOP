"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from aviaSales import views


urlpatterns = [
    path('', views.FlightListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('register_passenger/', views.register_passenger, name='register_passenger'),
    path('register_customer/', views.register_administrator, name='register_administrator'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),

    path('flights/', views.FlightListView.as_view(), name='flights'),
    re_path(r'user/?username=request.user.username/bookings/', views.UserBookingListView.as_view(), name='user_bookings'),  
    path('bookings/<int:number>/cancel/', views.cancel_booking, name='cancel_booking'),   
    path('bookings/<int:number>/edit_status', views.edit_booking_status, name='edit_booking_status'),
    path('bookings/<int:number>/delete', views.delete_booking, name='delete_booking'),
    path('bookings/all/', views.get_all_bookings, name='all_bookings'),

    path('flights/<int:current_flight_id>/booking/create/', views.BookingCreateView.as_view(), name='create_booking'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
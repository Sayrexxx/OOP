import requests
import random

from celery import shared_task
from .models.flight import Flight
from datetime import datetime

@shared_task
def fetch_and_save_flights():
    url = 'http://api.aviationstack.com/v1/flights?access_key=5283a72fcb0933e27a99a1c156d8c03a&airline_name=American%20Airlines'
    response = requests.get(url)
    data = response.json()
    
    flights_data = data.get('data', [])
    
    for flight in flights_data:
        flight_info = flight['flight']
        departure = flight['departure']
        arrival = flight['arrival']
        
        flight_number = flight_info['number']
        origin_point = departure['airport']
        destination_point = arrival['airport']
        departure_time = departure['scheduled']
        arrival_time = arrival['scheduled']
        available_seats = random.randint(50, 200)
        price = format(random.random() * 1000 + 500, ".2f")
        
        Flight.objects.update_or_create(
            number=flight_number,
            defaults={
                'origin_point': origin_point,
                'destination_point': destination_point,
                'departure_time': datetime.fromisoformat(departure_time),
                'arrival_time': datetime.fromisoformat(arrival_time),
                'available_seats': available_seats,
                'price': price
            }
        )

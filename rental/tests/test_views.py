import pytest
from django.urls import reverse
from datetime import date, timedelta
from rental.models import Vehicle, Booking, Customer

@pytest.mark.django_db
class TestVehicleViews:
    
    def setup_method(self):
        self.vehicle = Vehicle.objects.create(make="Honda", model="Civic", daily_rate=40.00)
    
    def test_vehicle_list_view(self, client):
        url = reverse('vehicle_list')
        response = client.get(url)
        assert response.status_code == 200
        assert b"Honda" in response.content

    def test_book_vehicle_get(self, client):
        url = reverse('book_vehicle', args=[self.vehicle.id])
        response = client.get(url)
        assert response.status_code == 200
        assert b"Book Honda Civic" in response.content

    def test_book_vehicle_post_valid(self, client):
        url = reverse('book_vehicle', args=[self.vehicle.id])
        
        start = date.today()
        end = start + timedelta(days=5)
        
        data = {
            'customer_name': 'Bob',
            'customer_age': '30',
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d'),
        }
        
        response = client.post(url, data)
        
        # Should redirect on success
        assert response.status_code == 302
        
        # Verify db created
        assert Customer.objects.count() == 1
        assert Booking.objects.count() == 1
        
        booking = Booking.objects.first()
        assert booking.customer.name == 'Bob'
        assert booking.state == 'CONFIRMED'
        # Base $40 * 5 = $200. No surcharge. No discount (<= 7 days, standard). Total $200.
        assert booking.total_price == 200.00

    def test_book_vehicle_post_invalid_age(self, client):
        url = reverse('book_vehicle', args=[self.vehicle.id])
        
        start = date.today()
        end = start + timedelta(days=5)
        
        data = {
            'customer_name': 'Tim',
            'customer_age': '19', # Too young
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d'),
        }
        
        response = client.post(url, data)
        
        # Should NOT redirect, should render form with error
        assert response.status_code == 200
        assert b"Must be at least 21" in response.content
        
        # Verify db NOT created
        assert Customer.objects.count() == 0
        assert Booking.objects.count() == 0

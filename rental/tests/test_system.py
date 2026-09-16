import pytest
import os
from datetime import date, timedelta
from .pages import VehicleListPage, BookingPage
from rental.models import Vehicle

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

@pytest.mark.django_db
def test_successful_booking_journey(page, live_server):
    # Setup data
    vehicle = Vehicle.objects.create(make="Ford", model="Focus", daily_rate=45.00)
    
    # Use Page Objects
    list_page = VehicleListPage(page)
    booking_page = BookingPage(page)
    
    # 1. Navigate to home
    list_page.navigate(live_server.url)
    assert list_page.get_vehicle_count() > 0
    
    # 2. Click book
    list_page.book_vehicle(vehicle.id)
    
    # 3. Fill out booking form
    start = date.today()
    end = start + timedelta(days=3)
    
    booking_page.fill_form(
        name="Charlie",
        age=28,
        is_premium=False,
        start_date=start.strftime('%Y-%m-%d'),
        end_date=end.strftime('%Y-%m-%d')
    )
    
    booking_page.submit()
    
    # 4. Verify success (redirected back to list and shows message)
    page.wait_for_selector(".success")
    assert "Booking confirmed!" in page.inner_text(".messages")

@pytest.mark.django_db
def test_failed_booking_journey_underage(page, live_server):
    # Setup data
    vehicle = Vehicle.objects.create(make="Nissan", model="Altima", daily_rate=55.00)
    
    # Use Page Objects
    list_page = VehicleListPage(page)
    booking_page = BookingPage(page)
    
    # 1. Navigate directly to booking page
    page.goto(f"{live_server.url}/book/{vehicle.id}/")
    
    # 2. Fill out booking form with underage user
    start = date.today()
    end = start + timedelta(days=2)
    
    booking_page.fill_form(
        name="Dave",
        age=19, # Underage
        is_premium=False,
        start_date=start.strftime('%Y-%m-%d'),
        end_date=end.strftime('%Y-%m-%d')
    )
    
    booking_page.submit()
    
    # 3. Verify error message on the same page
    page.wait_for_selector("#error-message")
    assert "Must be at least 21" in booking_page.get_error_message()

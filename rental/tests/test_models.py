import pytest
from datetime import date, timedelta
from rental.models import Customer, Vehicle, Booking
from rental.business_logic import BookingManager, BookingState, RentalCalculator

@pytest.mark.django_db
class TestBookingIntegration:
    
    def setup_method(self):
        self.customer = Customer.objects.create(name="Alice", age=22, is_premium=True)
        self.vehicle = Vehicle.objects.create(make="Toyota", model="Corolla", daily_rate=50.00)
        
        # 5 days rental
        start = date.today()
        end = start + timedelta(days=5)
        
        self.booking = Booking.objects.create(
            customer=self.customer,
            vehicle=self.vehicle,
            start_date=start,
            end_date=end
        )

    def test_booking_creation_default_state(self):
        assert self.booking.state == BookingState.REQUESTED
        assert self.booking.duration_days == 5

    def test_state_machine_integration(self):
        manager = BookingManager(current_state=self.booking.state)
        
        # Transition to confirmed
        new_state = manager.transition_to(BookingState.CONFIRMED)
        self.booking.state = new_state
        self.booking.save()
        
        # Verify saved in DB
        booking_from_db = Booking.objects.get(id=self.booking.id)
        assert booking_from_db.state == BookingState.CONFIRMED

    def test_pricing_integration(self):
        calc = RentalCalculator()
        
        # Alice is 22 (Young driver surcharge $20)
        # Vehicle is $50/day. Total rate: $70/day.
        # Duration: 5 days. Subtotal: $350.
        # Premium member, but <= 7 days -> 5% discount.
        # Discount: $350 * 0.05 = $17.50
        # Total: $332.50
        
        price = calc.calculate_price(
            age=self.booking.customer.age,
            duration_days=self.booking.duration_days,
            is_premium=self.booking.customer.is_premium
        )
        
        self.booking.total_price = price
        self.booking.save()
        
        assert self.booking.total_price == 332.50

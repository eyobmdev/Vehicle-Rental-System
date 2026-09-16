import pytest
from unittest.mock import MagicMock
from rental.business_logic import (
    RentalCalculator, BookingManager, BookingState, EmailService,
    AgeRestrictionError, DurationRestrictionError, InvalidStateTransitionError
)

class TestRentalCalculator:
    def setup_method(self):
        self.calc = RentalCalculator()

    # --- Equivalence Partitioning & Boundary Value Analysis (Age) ---
    def test_age_below_minimum(self):
        with pytest.raises(AgeRestrictionError):
            self.calc.calculate_price(age=20, duration_days=5)
            
    def test_age_at_minimum_with_surcharge(self):
        # Age 21: $50 + $20 surcharge = $70/day. $70 * 5 = 350. No discount -> 350.0
        price = self.calc.calculate_price(age=21, duration_days=5)
        assert price == 350.0

    def test_age_just_below_standard_rate(self):
        # Age 24: $50 + $20 surcharge = $70/day. $70 * 5 = 350. No discount -> 350.0
        price = self.calc.calculate_price(age=24, duration_days=5)
        assert price == 350.0

    def test_age_at_standard_rate(self):
        # Age 25: $50/day. $50 * 5 = 250. No discount -> 250.0
        price = self.calc.calculate_price(age=25, duration_days=5)
        assert price == 250.0

    # --- Equivalence Partitioning & Boundary Value Analysis (Duration) ---
    def test_duration_zero(self):
        with pytest.raises(DurationRestrictionError):
            self.calc.calculate_price(age=30, duration_days=0)

    def test_duration_minimum_valid(self):
        price = self.calc.calculate_price(age=30, duration_days=1)
        assert price == 50.0

    def test_duration_maximum_valid(self):
        price = self.calc.calculate_price(age=30, duration_days=30)
        assert price == 1350.0  # 50 * 30, > 7 days = 10% discount -> 1500 - 150 = 1350.0

    def test_duration_above_maximum(self):
        with pytest.raises(DurationRestrictionError):
            self.calc.calculate_price(age=30, duration_days=31)

    # --- Decision Table Testing (Discounts) ---
    # C1: Premium, C2: > 7 days
    def test_discount_premium_long_duration(self):
        # Base: $50 * 10 = $500. Discount: 20% = $100. Total: $400
        price = self.calc.calculate_price(age=30, duration_days=10, is_premium=True)
        assert price == 400.0

    def test_discount_premium_short_duration(self):
        # Base: $50 * 5 = $250. Discount: 5% = $12.5. Total: $237.5
        price = self.calc.calculate_price(age=30, duration_days=5, is_premium=True)
        assert price == 237.5

    def test_discount_standard_long_duration(self):
        # Base: $50 * 10 = $500. Discount: 10% = $50. Total: $450
        price = self.calc.calculate_price(age=30, duration_days=10, is_premium=False)
        assert price == 450.0

    def test_discount_standard_short_duration(self):
        # Base: $50 * 5 = $250. Discount: 0% = $0. Total: $250
        price = self.calc.calculate_price(age=30, duration_days=5, is_premium=False)
        assert price == 250.0

class TestBookingManager:
    # --- State Transition Testing ---
    def test_valid_transitions_to_success(self):
        manager = BookingManager()
        assert manager.state == BookingState.REQUESTED
        
        manager.transition_to(BookingState.CONFIRMED)
        assert manager.state == BookingState.CONFIRMED
        
        manager.transition_to(BookingState.ACTIVE)
        assert manager.state == BookingState.ACTIVE
        
        manager.transition_to(BookingState.RETURNED)
        assert manager.state == BookingState.RETURNED

    def test_valid_transition_to_cancelled_from_requested(self):
        manager = BookingManager()
        manager.transition_to(BookingState.CANCELLED)
        assert manager.state == BookingState.CANCELLED

    def test_valid_transition_to_cancelled_from_confirmed(self):
        manager = BookingManager()
        manager.transition_to(BookingState.CONFIRMED)
        manager.transition_to(BookingState.CANCELLED)
        assert manager.state == BookingState.CANCELLED

    def test_invalid_transition_requested_to_active(self):
        manager = BookingManager()
        with pytest.raises(InvalidStateTransitionError):
            manager.transition_to(BookingState.ACTIVE)

    def test_invalid_transition_from_cancelled(self):
        manager = BookingManager(current_state=BookingState.CANCELLED)
        with pytest.raises(InvalidStateTransitionError):
            manager.transition_to(BookingState.REQUESTED)

    # --- Test Double (Mock/Spy) ---
    def test_booking_manager_uses_collaborator_on_confirm(self):
        # Create a mock (test double) for the EmailService collaborator
        mock_email_service = MagicMock(spec=EmailService)
        
        # Inject the mock into the unit under test
        manager = BookingManager(current_state=BookingState.REQUESTED, email_service=mock_email_service)
        
        # Action
        manager.transition_to(BookingState.CONFIRMED)
        
        # Assert the collaborator was called correctly
        mock_email_service.send_confirmation.assert_called_once_with("Your booking is confirmed.")

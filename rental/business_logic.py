class AgeRestrictionError(Exception):
    pass

class DurationRestrictionError(Exception):
    pass

class InvalidStateTransitionError(Exception):
    pass


class RentalCalculator:
    BASE_RATE = 50.0  # $50 per day
    YOUNG_DRIVER_SURCHARGE = 20.0  # $20 per day

    def calculate_price(self, age: int, duration_days: int, is_premium: bool = False) -> float:
        # 1. Boundary Value & Equivalence Partitioning - Age
        if age < 21:
            raise AgeRestrictionError("Must be at least 21 to rent a vehicle.")
        
        # 2. Boundary Value & Equivalence Partitioning - Duration
        if duration_days <= 0:
            raise DurationRestrictionError("Duration must be at least 1 day.")
        if duration_days > 30:
            raise DurationRestrictionError("Maximum rental period is 30 days.")

        # Calculate base daily rate
        daily_rate = self.BASE_RATE
        if 21 <= age < 25:
            daily_rate += self.YOUNG_DRIVER_SURCHARGE

        subtotal = daily_rate * duration_days

        # 3. Decision Table - Discount Logic
        # C1: Premium Member?
        # C2: Duration > 7 days?
        discount_multiplier = 0.0
        
        if is_premium and duration_days > 7:
            discount_multiplier = 0.20  # 20%
        elif is_premium and duration_days <= 7:
            discount_multiplier = 0.05  # 5%
        elif not is_premium and duration_days > 7:
            discount_multiplier = 0.10  # 10%
        else:
            discount_multiplier = 0.0   # 0%

        discount_amount = subtotal * discount_multiplier
        total_price = subtotal - discount_amount

        return round(total_price, 2)

class BookingState:
    REQUESTED = "REQUESTED"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"

class EmailService:
    def send_confirmation(self, message: str):
        # In a real app, this would send an email over SMTP
        print(f"Sending email: {message}")
        return True

class BookingManager:
    # 4. State Transition Logic
    VALID_TRANSITIONS = {
        BookingState.REQUESTED: [BookingState.CONFIRMED, BookingState.CANCELLED],
        BookingState.CONFIRMED: [BookingState.ACTIVE, BookingState.CANCELLED],
        BookingState.ACTIVE: [BookingState.RETURNED],
        BookingState.RETURNED: [],
        BookingState.CANCELLED: []
    }

    def __init__(self, current_state=BookingState.REQUESTED, email_service=None):
        self.state = current_state
        # Inject dependency (collaborator)
        self.email_service = email_service or EmailService()

    def transition_to(self, new_state: str):
        if new_state not in self.VALID_TRANSITIONS.get(self.state, []):
            raise InvalidStateTransitionError(f"Cannot transition from {self.state} to {new_state}")
        
        self.state = new_state
        
        # Trigger collaborator on CONFIRMED
        if self.state == BookingState.CONFIRMED:
            self.email_service.send_confirmation("Your booking is confirmed.")
            
        return self.state

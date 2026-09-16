from django.db import models
from .business_logic import BookingState

class Customer(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.make} {self.model}"


class Booking(models.Model):
    STATE_CHOICES = [
        (BookingState.REQUESTED, 'Requested'),
        (BookingState.CONFIRMED, 'Confirmed'),
        (BookingState.ACTIVE, 'Active'),
        (BookingState.RETURNED, 'Returned'),
        (BookingState.CANCELLED, 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=BookingState.REQUESTED)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking {self.id} - {self.customer.name} - {self.vehicle.make}"

    @property
    def duration_days(self):
        if self.end_date and self.start_date:
            return (self.end_date - self.start_date).days
        return 0

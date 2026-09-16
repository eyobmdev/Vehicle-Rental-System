from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from .models import Vehicle, Customer, Booking
from .business_logic import RentalCalculator, BookingManager, AgeRestrictionError, DurationRestrictionError

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'rental/vehicle_list.html', {'vehicles': vehicles})

def book_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        age_str = request.POST.get('customer_age')
        is_premium = request.POST.get('is_premium') == 'on'
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        try:
            age = int(age_str)
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            duration_days = (end_date - start_date).days
            
            # Use our core OOP logic to validate and price
            calc = RentalCalculator()
            # We must set the BASE_RATE dynamically to the vehicle's rate
            calc.BASE_RATE = float(vehicle.daily_rate)
            
            price = calc.calculate_price(age, duration_days, is_premium)
            
            # If we get here, validation passed. Create records.
            customer = Customer.objects.create(name=name, age=age, is_premium=is_premium)
            
            booking = Booking.objects.create(
                customer=customer,
                vehicle=vehicle,
                start_date=start_date,
                end_date=end_date,
                total_price=price
            )
            
            # Transition state to confirmed
            manager = BookingManager(current_state=booking.state)
            booking.state = manager.transition_to('CONFIRMED')
            booking.save()
            
            messages.success(request, f"Booking confirmed! Total price: ${price:.2f}")
            return redirect('vehicle_list')
            
        except (AgeRestrictionError, DurationRestrictionError) as e:
            return render(request, 'rental/booking_form.html', {'vehicle': vehicle, 'error': str(e)})
        except ValueError:
            return render(request, 'rental/booking_form.html', {'vehicle': vehicle, 'error': "Invalid input formats."})

    return render(request, 'rental/booking_form.html', {'vehicle': vehicle})

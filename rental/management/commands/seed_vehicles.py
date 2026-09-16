from django.core.management.base import BaseCommand
from rental.models import Vehicle

class Command(BaseCommand):
    help = 'Seeds the database with initial vehicles'

    def handle(self, *args, **options):
        vehicles_data = [
            {'make': 'Toyota', 'model': 'Camry', 'daily_rate': 45.00, 'is_available': True},
            {'make': 'Honda', 'model': 'Accord', 'daily_rate': 50.00, 'is_available': True},
            {'make': 'Ford', 'model': 'Mustang', 'daily_rate': 85.00, 'is_available': True},
            {'make': 'Tesla', 'model': 'Model 3', 'daily_rate': 95.00, 'is_available': True},
            {'make': 'BMW', 'model': 'X5', 'daily_rate': 120.00, 'is_available': False},
            {'make': 'Jeep', 'model': 'Wrangler', 'daily_rate': 70.00, 'is_available': True},
        ]

        # Clear existing to avoid duplicates if run multiple times
        Vehicle.objects.all().delete()

        for data in vehicles_data:
            Vehicle.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Successfully created vehicle: {data["make"]} {data["model"]}'))
            
        self.stdout.write(self.style.SUCCESS(f'Database seeded with {len(vehicles_data)} vehicles.'))

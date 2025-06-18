from django.core.management.base import BaseCommand
from iniyathalaimurai.models import ServiceCategory, Service

class Command(BaseCommand):
    help = 'Preload service categories and service names'

    def handle(self, *args, **kwargs):
        service_data = {
            "Aadhaar": [
                "Enrolment",
                "Update - Name",
                "Update - DOB",
                "Update - Biometric",
                "Update - Mobile",
                "Update - Email",
            ],
            "PAN": [
                "Enrolment",
                "Update - Name",
                "Update - DOB",
            ],
            "Voter ID": [
                "Enrolment",
                "Update - Name",
                "Update - DOB",
                "Update - Address",
            ],
            "Driving Licence": [
                "Enrolment",
                "Update - Name",
                "Update - DOB",
                "Update - Address",
            ],
            "Ration Card": [
                "Enrolment",
                "Update - Add Family Member",
                "Update - Remove Family Member",
                "Update - Address",
            ]
        }

        for category_name, service_names in service_data.items():
            category, _ = ServiceCategory.objects.get_or_create(name=category_name)
            for service_name in service_names:
                Service.objects.get_or_create(category=category, name=service_name)

        self.stdout.write(self.style.SUCCESS('✅ All services preloaded successfully!'))

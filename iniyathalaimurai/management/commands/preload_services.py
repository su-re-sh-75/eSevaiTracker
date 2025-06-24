import os
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from iniyathalaimurai.models import ServiceCategory, Service

class Command(BaseCommand):
    help = 'Preload service categories, images, prices, and service names'

    def handle(self, *args, **kwargs):
        service_data = {
            "Aadhaar": {
                "image": "aadhaar.png",
                "services": [
                    ("Enrolment", 100),
                    ("Update - Name", 50),
                    ("Update - DOB", 50),
                    ("Update - Biometric", 80),
                    ("Update - Mobile", 40),
                    ("Update - Email", 40),
                ]
            },
            "PAN": {
                "image": "pan.jpg",
                "services": [
                    ("Enrolment", 100),
                    ("Update - Name", 60),
                    ("Update - DOB", 60),
                ]
            },
            "Voter ID": {
                "image": "voter_ID.jpg",
                "services": [
                    ("Enrolment", 90),
                    ("Update - Name", 50),
                    ("Update - DOB", 50),
                    ("Update - Address", 60),
                ]
            },
            "Driving Licence": {
                "image": "DL.jpeg",
                "services": [
                    ("Enrolment", 120),
                    ("Update - Name", 70),
                    ("Update - DOB", 70),
                    ("Update - Address", 80),
                ]
            },
            "Ration Card": {
                "image": "Ration-Card.jpg",
                "services": [
                    ("Enrolment", 100),
                    ("Update - Add Family Member", 50),
                    ("Update - Remove Family Member", 50),
                    ("Update - Address", 60),
                ]
            }
        }

        for category_name, data in service_data.items():
            category, _ = ServiceCategory.objects.get_or_create(name=category_name)

            if not category.image:
                img_path = os.path.join(settings.MEDIA_ROOT, 'service_images', data['image'])
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        category.image.save(data['image'], File(f), save=True)

            for service_name, price in data['services']:
                Service.objects.update_or_create(
                    category=category,
                    name=service_name,
                    defaults={'price': price}
                )

        self.stdout.write(self.style.SUCCESS('✅ All service categories, images, and service names preloaded successfully!'))
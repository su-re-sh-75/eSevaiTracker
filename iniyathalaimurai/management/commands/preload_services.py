import os
from django.core.files import File
from django.conf import settings
from django.core.management.base import BaseCommand
from iniyathalaimurai.models import ServiceCategory, Service

class Command(BaseCommand):
    help = 'Preload service categories, images, and service names'

    def handle(self, *args, **kwargs):
        service_data = {
            "Aadhaar": {
                "services": [
                    "Enrolment",
                    "Update - Name",
                    "Update - DOB",
                    "Update - Biometric",
                    "Update - Mobile",
                    "Update - Email",
                ],
                "image": "aadhaar.png"
            },
            "PAN": {
                "services": [
                    "Enrolment",
                    "Update - Name",
                    "Update - DOB",
                ],
                "image": "pan.jpg"
            },
            "Voter ID": {
                "services": [
                    "Enrolment",
                    "Update - Name",
                    "Update - DOB",
                    "Update - Address",
                ],
                "image": "voter_ID.jpg"
            },
            "Driving Licence": {
                "services": [
                    "Enrolment",
                    "Update - Name",
                    "Update - DOB",
                    "Update - Address",
                ],
                "image": "DL.jpeg"
            },
            "Ration Card": {
                "services": [
                    "Enrolment",
                    "Update - Add Family Member",
                    "Update - Remove Family Member",
                    "Update - Address",
                ],
                "image": "Ration-Card.jpg"
            }
        }

        for category_name, data in service_data.items():
            category, created = ServiceCategory.objects.get_or_create(name=category_name)

            # Add image if not already set
            if not category.image:
                image_path = os.path.join(settings.MEDIA_ROOT, 'service_images', data['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        category.image.save(data['image'], File(img_file), save=True)

            for service_name in data['services']:
                Service.objects.get_or_create(category=category, name=service_name)

        self.stdout.write(self.style.SUCCESS('✅ All service categories, images, and service names preloaded successfully!'))

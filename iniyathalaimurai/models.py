from django.db import models
from users.models import User

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True) # Aadhaar, PAN, VoterId, Driving Licence, Ration Card

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)  # e.g. "enrolment", "update - name"
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    payment = models.OneToOneField('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    userPaymentStatus = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('not_paid', 'Not Paid')], default='not_paid')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    userAppliedAt = models.DateTimeField(auto_now_add=True)
    applicationAppliedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application {self.applicationID} - {self.service}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('verifying', 'Verifying'),
        ('accepted', 'Accepted'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='verifying')
    paidAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.paymentID} - {self.status}"

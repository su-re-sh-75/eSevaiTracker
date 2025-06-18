from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom manager
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_num, password, name=None):
        if not phone_num:
            raise ValueError("Users must have a phone number")
        user = self.model(phone_num=phone_num, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_num, password, name=None):
        user = self.create_user(phone_num=phone_num, name=name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    phone_num = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_num'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_num

# Docs Model
class Document(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='documents')
    aadhaar_num = models.CharField(max_length=20, blank=True, null=True)
    pan_num = models.CharField(max_length=20, blank=True, null=True)
    voter_id = models.CharField(max_length=20, blank=True, null=True)

    aadhaar_file = models.FileField(upload_to='docs/aadhaar/', blank=True, null=True)
    pan_file = models.FileField(upload_to='docs/pan/', blank=True, null=True)
    voterid_file = models.FileField(upload_to='docs/voterid/', blank=True, null=True)
    driving_license_file = models.FileField(upload_to='docs/driving_license/', blank=True, null=True)
    ration_card_file = models.FileField(upload_to='docs/ration_card/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.phone_num}'s Documents"

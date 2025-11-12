from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("producer", "Producer"),
        ("consumer", "Consumer"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    code_pin = models.CharField(max_length=6, blank=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_picture/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)
    
    # Farm information for producers
    farm_name = models.CharField(max_length=255, blank=True, null=True)
    farm_address = models.TextField(blank=True, null=True)
    farm_description = models.TextField(blank=True, null=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_generated_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'auth_user'  # Optionnel, pour éviter les conflits

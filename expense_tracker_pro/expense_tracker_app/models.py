from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,email,name,phone,password=None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone = phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,name,phone,password):
        user = self.create_user(email,name,phone,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone']

    def __str__(self):
        return self.email
    
class Expense(models.Model):
    CATEGORIES = [
        ('FOOD','Food'),
        ('TRAVEL','Travel'),
        ('UTILITIES','Utilities'),
        ('ENTERTAINMENT','Entertainment'),
        ('OTHER','Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.email} -{self.category}, {self.amount}kg on {self.date}"
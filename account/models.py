from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from common.models import AuditableModel
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Email field must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, AuditableModel, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=255, blank=True)
    last_name = models.CharField('last name', max_length=255, blank=True)
    middle_name = models.CharField('middle name', max_length=255, blank=True)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)
    is_staff = models.BooleanField(default=False)
    reset_password_token = models.CharField(null=True,blank=True, max_length=125)
    profile_image = models.URLField(null=True, blank=True)
    telephone = models.CharField('telephone', unique=False, null=True, blank=True, max_length=255)
    address_line_1 = models.CharField('address_line_1',null=True, blank=True, max_length=255)
    reset_code = models.CharField(max_length=256, null=True, blank=True)
    push_notification_token = models.CharField(max_length=256, null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()
    all_objects = models.Manager()

    @property
    def is_admin(self):
        return self.is_superuser

    def __str__(self):
        return f'{self.email} {self.last_name or ""}'.strip()
    
    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()


class Player(AuditableModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.FileField(null=True, blank=True)
    position = models.CharField(max_length=255)
    notes = models.TextField()
    

class UserPlayer(AuditableModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    player =models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

  
class PlaySchedule(AuditableModel):
    venue = models.CharField(max_length=255)
    date = models.DateField(auto_now=False, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()     


class PlayerAttendance(AuditableModel):
    player = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING
    )
    schedule = models.ForeignKey(
        PlaySchedule,
        on_delete=models.DO_NOTHING
    )
    notes = models.TextField()
    

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        nama,
        no_hp=None,
        role="petugas",
        password=None,
        **extra_fields,
    ):
        if not username:
            raise ValueError("Username harus diisi.")

        if not nama:
            raise ValueError("Nama harus diisi.")

        extra_fields.pop("role", None)

        user = self.model(
            username=username,
            nama=nama,
            no_hp=no_hp,
            role=role,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nama, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            username=username,
            nama=nama,
            password=password,
            role="admin",
            **extra_fields,
        )

        # user.is_superuser = True
        # user.is_staff = (True,)
        # user.save(using=self._db)
        # return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("petugas", "Petugas Lapangan"),
    )

    user_id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=150)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="petugas")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nama"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Daftar User"

    def __str__(self):
        return f"{self.nama} ({self.role})"

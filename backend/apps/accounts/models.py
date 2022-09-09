from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Company(models.Model):
    name = models.CharField("社名", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class Department(models.Model):
    name = models.CharField("部門名", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Departments"


class Section(models.Model):
    name = models.CharField("課名", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sections"


class Position(models.Model):
    name = models.CharField("役職", max_length=255, unique=True)
    access_level = models.IntegerField("権限レベル")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Positions"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')

        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("メールアドレス", max_length=255, unique=True)
    first_name = models.CharField("姓", max_length=255)
    last_name = models.CharField("名", max_length=255)
    user_number = models.IntegerField("社員番号")
    company = models.ForeignKey(Company, on_delete=models.PROTECT,
                                verbose_name="所属会社", blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, verbose_name="所属部門", blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.PROTECT,
                                verbose_name="所属課", blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT,
                                 verbose_name="役職", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_number']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "CustomUsers"
        verbose_name = "CustomUser"

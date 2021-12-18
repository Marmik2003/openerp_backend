from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from simple_history.models import HistoricalRecords


# Create your models here.
class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.
    """

    use_in_migrations = True

    def _create_user(self, email, first_name, phone, password, **extra_fields):
        values = [email, first_name, phone]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, phone, password, **extra_fields)

    def create_superuser(self, email, first_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, first_name, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    """

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, unique=True)
    is_business_owner = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='user_avatars')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    history = HistoricalRecords()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def get_full_name(self):
        if self.last_name is not None:
            return self.first_name + ' ' + self.last_name
        else:
            return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()


class Subscription(models.Model):
    """
    A subscription is a plan that a business can subscribe to.
    """

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Business(models.Model):
    """
    A business is a company that owns the ERP account.
    Business accounts are on subscription basis.
    """

    name = models.CharField(max_length=50)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=16)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='business_avatars')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class EmployeeGroup(models.Model):
    """
    An employee group is a group of employees that work together.
    """

    name = models.CharField(max_length=50)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EmployeeType(models.Model):
    """
    An employee type is a type of employee.
    """

    type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    group = models.ForeignKey(EmployeeGroup, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class EmployeeTypePermission(models.Model):
    """
    A group permission is a permission that is given to a group.
    """

    class DefaultPermissionChoice(models.TextChoices):
        VIEW = 'view', 'View'
        COMMENT = 'comment', 'Comment'
        EDIT = 'edit', 'Edit'
        FULL_ACCESS = 'full_access', 'Full Access'

    class ClaimPermissionChoices(models.TextChoices):
        VIEW = 'view', 'View'
        CHANGE = 'change', 'Change'

    employee_type = models.OneToOneField(EmployeeType, on_delete=models.CASCADE)
    project_access = models.CharField(
        max_length=11,
        choices=DefaultPermissionChoice.choices,
        default=DefaultPermissionChoice.VIEW
    )
    sales_access = models.CharField(
        max_length=11,
        choices=DefaultPermissionChoice.choices,
        default=DefaultPermissionChoice.VIEW
    )
    pos_access = models.CharField(
        max_length=11,
        choices=DefaultPermissionChoice.choices,
        default=DefaultPermissionChoice.VIEW
    )
    inventory_access = models.CharField(
        max_length=11,
        choices=DefaultPermissionChoice.choices,
        default=DefaultPermissionChoice.VIEW
    )
    customer_access = models.CharField(
        max_length=11,
        choices=DefaultPermissionChoice.choices,
        default=DefaultPermissionChoice.VIEW
    )
    claim_access = models.CharField(
        max_length=10,
        choices=ClaimPermissionChoices.choices,
        default=ClaimPermissionChoices.VIEW
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee_type.type + ' Permissions'


class Employee(models.Model):
    """
    An employee is a person who works for a business.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.CASCADE, null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()

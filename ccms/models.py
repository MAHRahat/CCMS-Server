from django.contrib.auth.models import AbstractUser
from django.db import models

from ccms.managers import CCMSUserManager


class CCMSUser(AbstractUser):
    """
    Custom user model for the City Complaints Management System.
    """
    user_id = models.AutoField(primary_key=True)
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, null=False, blank=False, db_column='email')
    cell_no = models.CharField(unique=True, max_length=14, null=True, blank=True)
    name = models.CharField(max_length=25, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_employee = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CCMSUserManager()

    class Meta:
        db_table = 'ccms_users'

    def __str__(self):
        if self.name is None:
            return f"{self.email}"
        else:
            return f"{self.name}"


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True, unique=True)
    category = models.CharField(max_length=25)
    keyword = models.CharField(max_length=25)

    class Meta:
        db_table = 'ccms_categories'

    def __str__(self):
        return f"{self.category} {self.keyword}"


class Complaints(models.Model):
    complaints_id = models.BigAutoField(primary_key=True, unique=True)
    time_submitted = models.DateTimeField(auto_now_add=True)
    time_last_updated = models.DateTimeField(auto_now=True)
    citizen_id = models.ForeignKey(CCMSUser, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=False)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    status = models.CharField(null=True, max_length=30, default='Submitted')
    location = models.TextField(null=True)

    class Meta:
        db_table = 'ccms_complaints'

    def __str__(self):
        return f"{self.description}"

    def citizen_name(self):
        return self.citizen_id.name

    def category_name(self):
        return self.category_id.category

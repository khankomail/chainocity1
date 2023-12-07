from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
import uuid
import random
import string
from django.utils.translation import gettext as _
from django.utils import timezone

class ChainUser(AbstractUser):

    id_string = models.CharField(max_length=255, unique=True)
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    dob = models.DateField(_('date of birth'), blank=True, null=True)
    referral_code_own = models.CharField(max_length=255, unique=True, blank=True, null=True)
    referral_code_other = models.CharField(max_length=8, blank=True, null=True)
    earning = models.IntegerField(default=0)
    package = models.CharField(max_length=50, choices=[('basic', 'Basic'), ('gold', 'Gold')], blank=True, null=True)
    referral_code_users = models.ManyToManyField('self', symmetrical=False, related_name='referral_codes', blank=True)
    code_users = models.IntegerField(default=0)

    def calculate_code_users(self):
        users_with_code = ChainUser.objects.filter(referral_code_other=self.referral_code_own)
        self.code_users = users_with_code.count()

    def save(self, *args, **kwargs):
        if not self.id_string:
            self.id_string = self.generate_unique_id()

        if not self.referral_code_own:
            self.referral_code_own = self.id_string

        self.calculate_code_users()

        super().save(*args, **kwargs)

    def generate_unique_id(self, length=8):
        # Generate a random string of uppercase letters and digits
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def save(self, *args, **kwargs):
        if not self.id_string:
            # Generate id_string using the same logic as referral_code_own
            self.id_string = self.generate_unique_id()

        if not self.referral_code_own:
            # Set referral_code_own to id_string
            self.referral_code_own = self.id_string

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    groups = models.ManyToManyField(
        Group, verbose_name=_('groups'), blank=True,
        related_name='chainuser_set',  # Add this line
        related_query_name='chainuser'
    )
    user_permissions = models.ManyToManyField(
        Permission, verbose_name=_('user permissions'), blank=True,
        related_name='chainuser_set',  # Add this line
        related_query_name='chainuser'
    )

    class Meta:
        app_label = 'myapp'


class Product(models.Model):
    p_id = models.CharField(max_length=5, unique=True, null=True, blank=True)
    p_title = models.CharField(max_length=255)
    p_stocked = models.BooleanField(default=True)
    p_description = models.TextField()
    p_price = models.DecimalField(max_digits=10, decimal_places=2 , default=0)
    p_img = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate p_id using the same logic as referral_code_own
        if not self.p_id:
            self.p_id = self.generate_unique_id()

        super().save(*args, **kwargs)

    def generate_unique_id(self, length=5):
        # Generate a random string of uppercase letters and digits
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(characters) for _ in range(length))

    def __str__(self):
        return self.p_title


class Payment(models.Model):
    transaction_id = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=2)  # Assuming 1 for success, 0 for failure, adjust as needed

    def __str__(self):
        return f"Payment {self.id} - Transaction ID: {self.transaction_id}"



def generate_random_string(length=5):
    """Generate a random string."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class Receipt(models.Model):
    r_id = models.CharField(max_length=5, default=generate_random_string, unique=True, editable=False)
    recipient = models.CharField(max_length=255)
    w_amount = models.FloatField()
    ave_balc = models.FloatField()
    acc_no = models.CharField(max_length=20, null=True)  # Adjust the max_length as needed
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"Receipt #{self.r_id} - {self.recipient}"

    
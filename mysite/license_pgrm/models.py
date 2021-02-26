from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime, date
from django.utils.timezone import now


class Organizations(models.Model):
    CUSTOMER = "customer"
    PARTNER = "partner"
    org_id = models.CharField(max_length=10, primary_key=True)
    org_name = models.CharField(max_length=100)
    ORG_TYPE_CHOICES = [
        (CUSTOMER, "Customer"),
        (PARTNER, "Partner"),
    ]
    org_type = models.CharField(max_length=8, choices=ORG_TYPE_CHOICES)
    domain = models.CharField(max_length=100)


class Entitlement(models.Model):
    orgid = models.ForeignKey(to=Organizations, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, primary_key=True)
    max_licenses = models.IntegerField()

    @property
    def total_licenses(self):
        return Entitlement.objects.filter(product_name=self.product_name, orgid=self.orgid).count()


class UserProfile(models.Model):
    ADMINISTRATOR = "admin"
    USER = "user"
    ACTIVE = "active"
    REMOVED = "removed"
    name = models.CharField(max_length=100, primary_key=True)
    phone_regex = RegexValidator(r"^\+?1?\d+$", "+##########")
    phone = models.CharField(validators=[phone_regex], max_length=12)

    ROLE_CHOICES = [

        (ADMINISTRATOR, "Administrator"),
        (USER, "User"),

    ]
    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (REMOVED, "Removed"),
        ]

    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default=USER)
    orgid = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(default=now())
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=ACTIVE)


class License(models.Model):
    orgid = models.ForeignKey(to=Organizations, on_delete=models.CASCADE)
    product_name = models.ForeignKey(to=Entitlement, on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    created_by = models.ForeignKey(to=UserProfile, to_field="email", on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.today())
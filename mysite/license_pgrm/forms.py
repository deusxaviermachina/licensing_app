from django import forms
from .models import UserProfile, License
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        fields = ["product_name", "version", "created_by", "orgid",
                  "created_at",
                  ]


class CustomProfileCreation(forms.Form):
    ROLE_CHOICES = (
        ("USER", "user"),
        ("ADMIN", "admin"),
    )
    STATUS_CHOICES = (
        ("ACTIVE", "active"),
        ("REMOVED", "removed"),
    )

    phone_regex = RegexValidator(r"^\+?1?\d+$", "format: +##########")
    phone = forms.CharField(validators=[phone_regex])
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    email = forms.EmailField()

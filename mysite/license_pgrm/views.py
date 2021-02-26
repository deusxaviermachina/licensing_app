from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime
from.models import License, UserProfile
from.forms import LicenseForm, CustomProfileCreation

def indexView(request):
    return render(request, "license_pgrm/index.html")

@login_required()
def dashboardView(request):
    return render(request,'license_pgrm/dashboard.html')

@login_required()
def signup(request):
    if request.method == "POST":
        login_creds = UserCreationForm(request.POST)
        extended_profile = CustomProfileCreation(request.POST)
        current_user = request.user
        if not current_user.groups.filter(name="admin").exists():
            raise PermissionError("You are not authorized to add users")
        else:
            pass
        if login_creds.is_valid() and extended_profile.is_valid():
            user = login_creds.save()
            user.refresh_from_db()
            current_user_orgid = UserProfile.objects.filter(name=current_user.username).all()[0].orgid
            profile = UserProfile(name=user, role=extended_profile["role"], phone=extended_profile["phone"],
                                  orgid=current_user_orgid, date_created=datetime.datetime.now(),
                                  status=extended_profile["status"], email=extended_profile["email"])
            profile.save()
            context = {
                "username": login_creds.cleaned_data["username"],
                "orgid": UserProfile.objects.filter(name=current_user.username).all()[0].orgid.org_name,
            }
            return render(request, "registration/userprofile_successfully_created.html", context=context)
    else:
        login_creds = UserCreationForm()
        extended_profile = CustomProfileCreation()
    return render(request, "registration/register.html", {'form1': login_creds, "form2": extended_profile})

@login_required()
def create_license(request):
    if request.method == "POST":
        form = LicenseForm(request.POST)
        current_user = request.user
        current_user_orgid = UserProfile.objects.filter(name=current_user.username).all()[0].orgid
        if form.is_valid():
            if form.cleaned_data["orgid"] != current_user_orgid:
                raise PermissionError("invalid user ID credentials")
            else:
                pass
            n_licenses = License.objects.filter(product_name=form.cleaned_data["product_name"].product_name).all()
            if n_licenses.count() >= form.cleaned_data["product_name"].total_licenses:
                raise PermissionError("max licensing exceeded")
            if current_user_orgid != form.cleaned_data["product_name"].orgid or current_user.username != form.cleaned_data["created_by"].name:
                raise PermissionError("mismatching credentials")
            else:
                pass
            profile = form.save()
            profile.refresh_from_db()
            context = {"product_name": form.cleaned_data["product_name"].product_name,
                       }
            return render(request, "license_pgrm/license_created_successfully.html", context=context)
    else:
        form = LicenseForm()
    return render(request, "license_pgrm/license_creation.html", {'form': form})
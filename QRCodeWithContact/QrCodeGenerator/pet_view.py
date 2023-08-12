import random
import string

from cryptography.fernet import Fernet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from .constants import (CONGRATULATION_MESSAGE, EMAIL_TYPE_FORGOT_PW, SALT,
                        SUBJECT_FOR_FORGOT_PASSWORD)
from .models import PetOwnerInfo
from .utils import send_mail


@never_cache
def save_edited_pet_details(request, qr_code_number):
    return save_details_in_model(request, qr_code_number)


@never_cache
def save_pet_details(request, qr_code_number):
    try:
        email = request.POST.get("email", "")
        pet_owner_info = PetOwnerInfo.objects.filter(email=email).first()
        if pet_owner_info:
            context = {
                    "error ": email
                    + " is already present please use different Email ID",
                    "pet_owner_info": pet_owner_info,
                }

            return render(
                request,
                "enter_pet_details.html",
                context,
            )
        else:
            return save_details_in_model(request, qr_code_number)
    except:
        return save_details_in_model(request, qr_code_number)


def save_details_in_model(request, qr_code_number):
    pet_owner_info = PetOwnerInfo.objects.filter(qr_code_number=qr_code_number).first()
    pet_owner_info.email = request.POST.get("email")
    pet_owner_info.pet_name = request.POST.get("pet_name")
    pet_owner_info.owner_full_name = request.POST.get("owner_full_name")
    pet_owner_info.contact_number = request.POST.get("contact_number")
    pet_owner_info.current_location_link = request.POST.get("current_location_link")
    pet_owner_info.zip_code = request.POST.get("zip_code")
    pet_owner_info.password = request.POST.get("password")
    pet_owner_info.save()
    return HttpResponse(CONGRATULATION_MESSAGE.format(pet_owner_info.pet_name))


def get_pet_login_page(request):
    return render(request, "pet_login.html")


@never_cache
def post_login_pet_page(request):
    email = request.POST.get("email")
    pet_owner_info = PetOwnerInfo.objects.filter(email=email).first()
    pet_owner_info.password = ""
    return render(request, "edit_pet_details.html", {"pet_owner_info": pet_owner_info})


def forgot_pet_password(request):
    email = request.POST.get("email", "")
    fernet_key = Fernet(SALT)
    try:
        pet_owner_info = PetOwnerInfo.objects.filter(email=email).first()
        if pet_owner_info:
            password = "".join(random.choices(string.ascii_letters, k=9))
            pet_owner_info.password = fernet_key.encrypt(
                password.encode("utf-8")
            ).decode("utf-8")
            pet_owner_info.save()
            send_mail(
                pet_owner_info.email,
                SUBJECT_FOR_FORGOT_PASSWORD,
                EMAIL_TYPE_FORGOT_PW,
                password=password,
            )
            return render(
                request,
                "pet_login.html",
                {"message": "Check your registered mail for new password"},
            )
    except:
        return render(request, "pet_login.html", {"error": "Please enter valid email"})


def get_forgot_pet_email(request):
    return render(request, "forgot_pet_email.html")

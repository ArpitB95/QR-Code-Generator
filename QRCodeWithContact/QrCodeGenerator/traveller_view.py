import random
import string

from cryptography.fernet import Fernet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from .constants import (CONGRATULATION_MESSAGE, EMAIL_TYPE_FORGOT_PW, SALT,
                        SUBJECT_FOR_FORGOT_PASSWORD)
from .models import TravellerInfo
from .utils import send_mail


@never_cache
def save_edited_traveller_details(request, qr_code_number):
    return save_details_in_model(request, qr_code_number)


@never_cache
def save_traveller_details(request, qr_code_number):
    try:
        email = request.POST.get("email", "")
        traveller_info = TravellerInfo.objects.filter(email=email).first()
        if traveller_info:
            context = {
                "error_message": email
                + " is already present please use different Email ID",
                "traveller_info": traveller_info,
            }
            return render(
                request,
                "enter_traveller_details.html",
                context,
            )
        else:
            return save_details_in_model(request, qr_code_number)
    except:
        return save_details_in_model(request, qr_code_number)


def save_details_in_model(request, qr_code_number):
    fernet_key = Fernet(SALT)
    traveller_info = TravellerInfo.objects.get(qr_code_number=qr_code_number)
    traveller_info.full_name = request.POST.get("full_name", traveller_info.full_name)
    traveller_info.contact_number = request.POST.get(
        "contact_number", traveller_info.contact_number
    )
    traveller_info.current_country = request.POST.get(
        "current_country", traveller_info.current_country
    )
    traveller_info.current_address = request.POST.get(
        "current_address", traveller_info.current_address
    )
    traveller_info.current_location_link = request.POST.get(
        "current_location_link", traveller_info.current_location_link
    )
    traveller_info.destination_country = request.POST.get(
        "destination_country", traveller_info.destination_country
    )
    traveller_info.destination_address = request.POST.get(
        "destination_address", traveller_info.destination_address
    )
    traveller_info.destination_location_link = request.POST.get(
        "destination_location_link", traveller_info.destination_location_link
    )
    traveller_info.email = request.POST.get("email", traveller_info.email)
    if request.POST.get("password", ""):
        traveller_info.password = fernet_key.encrypt(
            request.POST.get("password", "").encode("utf-8")
        ).decode("utf-8")

    traveller_info.save()
    return HttpResponse(CONGRATULATION_MESSAGE.format(traveller_info.full_name))


@never_cache
def get_traveller_login_page(request):
    return render(request, "traveller_login.html")


@never_cache
def post_login_traveller_page(request):
    fernet_key = Fernet(SALT)
    email = request.POST.get("email", "")
    try:
        traveller_info = TravellerInfo.objects.filter(email=email).first()
        if (
            request.POST.get("password", "")
            == fernet_key.decrypt(traveller_info.password.encode("utf-8")).decode()
        ):
            traveller_info.password = ""
            return render(
                request,
                "edit_traveller_details.html",
                {"traveller_info": traveller_info},
            )
        return render(
            request,
            "traveller_login.html",
            {"error": "Please enter valid email and password"},
        )
    except Exception as e:
        return render(
            request,
            "traveller_login.html",
            {"error": "Please enter valid email and password"},
        )


def get_forgot_traveller_email(request):
    return render(request, "forgot_traveller_email.html")


def forgot_traveller_password(request):
    email = request.POST.get("email", "")
    fernet_key = Fernet(SALT)
    try:
        traveller_info = TravellerInfo.objects.filter(email=email).first()
        if traveller_info:
            password = "".join(random.choices(string.ascii_letters, k=9))
            traveller_info.password = fernet_key.encrypt(
                password.encode("utf-8")
            ).decode("utf-8")
            traveller_info.save()
            send_mail(
                traveller_info.email,
                SUBJECT_FOR_FORGOT_PASSWORD,
                EMAIL_TYPE_FORGOT_PW,
                password=password,
            )
            return render(
                request,
                "traveller_login.html",
                {"message": "Check your registered mail for new password"},
            )
    except:
        return render(
            request, "traveller_login.html", {"error": "Please enter valid email"}
        )

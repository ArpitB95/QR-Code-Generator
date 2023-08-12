import random
import string

from cryptography.fernet import Fernet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from .constants import (CONGRATULATION_MESSAGE, EMAIL_TYPE_FORGOT_PW, SALT,
                        SUBJECT_FOR_FORGOT_PASSWORD)
from .models import UserInfo
from .utils import send_mail


@never_cache
def save_edited_user_details(request, qr_code_number):
    return save_details_in_model(request, qr_code_number)


@never_cache
def save_user_details(request, qr_code_number):
    try:
        email = request.POST.get("email", "")
        user_info = UserInfo.objects.filter(email=email).first()
        if user_info:
            context = {
                "error_message": email
                + " is already present please use different Email ID",
                "user_info": user_info,
            }
            return render(
                request,
                "enter_user_details.html",
                context,
            )
        else:
            return save_details_in_model(request, qr_code_number)
    except:
        return save_details_in_model(request, qr_code_number)


def save_details_in_model(request, qr_code_number):
    fernet_key = Fernet(SALT)
    user_info = UserInfo.objects.get(qr_code_number=qr_code_number)
    user_info.full_name = request.POST.get("full_name", user_info.full_name)
    user_info.contact_number = request.POST.get(
        "contact_number", user_info.contact_number
    )
    user_info.address = request.POST.get("address", user_info.address)
    user_info.email = request.POST.get("email", user_info.email)
    if request.POST.get("password", ""):
        user_info.password = fernet_key.encrypt(
            request.POST.get("password", "").encode("utf-8")
        ).decode("utf-8")
    user_info.mother_name = request.POST.get("mother_name", user_info.mother_name)
    user_info.mother_contact_number = request.POST.get(
        "mother_contact_number", user_info.mother_contact_number
    )
    user_info.father_name = request.POST.get("father_name", user_info.father_name)
    user_info.father_contact_number = request.POST.get(
        "father_contact_number", user_info.father_contact_number
    )
    user_info.wife_name = request.POST.get("wife_name", user_info.wife_name)
    user_info.wife_contact_number = request.POST.get(
        "wife_contact_number", user_info.wife_contact_number
    )
    user_info.husband_name = request.POST.get("husband_name", user_info.husband_name)
    user_info.husband_contact_number = request.POST.get(
        "husband_contact_number", user_info.husband_contact_number
    )
    user_info.education_institute = request.POST.get(
        "education_institute", user_info.education_institute
    )
    user_info.education_institute_contact = request.POST.get(
        "education_institute_contact", user_info.education_institute_contact
    )
    user_info.work_place_name = request.POST.get(
        "work_place_name", user_info.work_place_name
    )
    user_info.work_place_address = request.POST.get(
        "work_place_address", user_info.work_place_address
    )
    user_info.best_friend_name = request.POST.get(
        "best_friend_name", user_info.best_friend_name
    )
    user_info.best_friend_contact_number = request.POST.get(
        "best_friend_contact_number", user_info.best_friend_contact_number
    )
    user_info.save()
    return HttpResponse(CONGRATULATION_MESSAGE.format(user_info.full_name))


@never_cache
def get_user_login_page(request):
    return render(request, "user_login.html")


@never_cache
def post_login_user_page(request):
    fernet_key = Fernet(SALT)
    email = request.POST.get("email", "")
    try:
        user_info = UserInfo.objects.filter(email=email).first()
        if (
            request.POST.get("password", "")
            == fernet_key.decrypt(user_info.password.encode("utf-8")).decode()
        ):
            user_info.password = ""
            return render(request, "edit_user_details.html", {"user_info": user_info})
        return render(
            request,
            "user_login.html",
            {"error": "Please enter valid email and password"},
        )
    except Exception as e:
        return render(
            request,
            "user_login.html",
            {"error": "Please enter valid email and password"},
        )


def get_forgot_user_email(request):
    return render(request, "forgot_user_email.html")


def forgot_user_password(request):
    email = request.POST.get("email", "")
    fernet_key = Fernet(SALT)
    try:
        user_info = UserInfo.objects.filter(email=email).first()
        if user_info:
            password = "".join(random.choices(string.ascii_letters, k=9))
            user_info.password = fernet_key.encrypt(password.encode("utf-8")).decode(
                "utf-8"
            )
            user_info.save()
            send_mail(
                user_info.email,
                SUBJECT_FOR_FORGOT_PASSWORD,
                EMAIL_TYPE_FORGOT_PW,
                password=password,
            )
            return render(
                request,
                "user_login.html",
                {"message": "Check your registered mail for new password"},
            )
    except:
        return render(request, "user_login.html", {"error": "Please enter valid email"})

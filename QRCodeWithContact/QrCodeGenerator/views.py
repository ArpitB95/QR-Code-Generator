from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserInfo
import string
import random
import smtplib
import bcrypt
import uuid

# Create your views here.

salt = b"$2b$12$tii0QHwvxAEWKUHrLtZSku"


def get_qr_code_details(request, qr_code_number):
    try:
        user_info = UserInfo.objects.filter(qr_code_number=qr_code_number).first()
        if user_info.email:
            return render(request, "view_user_details.html", {"user_info": user_info})
        return render(request, "enter_user_details.html", {"user_info": user_info})
    except:
        return render(request, "enter_user_details.html", {"user_info": user_info})


def save_user_details(request, qr_code_number):
    try:
        email = request.POST.get("email", "")
        user_info = UserInfo.objects.filter(email=email).first()
        if user_info:
            user_info = UserInfo.objects.filter(qr_code_number=qr_code_number).first()
            return render(
                request,
                "enter_user_details.html",
                {
                    "error ": email
                    + " is already present please use different Email ID",
                    "user_info": user_info,
                },
            )
    except:
        user_info = UserInfo.objects.get(id=id)
        user_info.full_name = request.POST.get("full_name", "")
        user_info.contact_number = request.POST.get("contact_number", "")
        user_info.address = request.POST.get("address", "")
        user_info.email = request.POST.get("email", "")
        user_info.password = bcrypt.hashpw(
            request.POST.get("password", "").encode("utf-8"), salt
        )
        user_info.mother_name = request.POST.get("mother_name", "")
        user_info.mother_contact_number = request.POST.get("mother_contact_number", "")
        user_info.father_name = request.POST.get("father_name", "")
        user_info.father_contact_number = request.POST.get("father_contact_number", "")
        user_info.wife_name = request.POST.get("wife_name", "")
        user_info.wife_contact_number = request.POST.get("wife_contact_number", "")
        user_info.husband_name = request.POST.get("husband_name", "")
        user_info.husband_contact_number = request.POST.get(
            "husband_contact_number", ""
        )
        user_info.education_institute = request.POST.get("education_institute", "")
        user_info.education_institute_contact = request.POST.get(
            "education_institute_contact", ""
        )
        user_info.work_place_name = request.POST.get("work_place_name", "")
        user_info.work_place_address = request.POST.get("work_place_address", "")
        user_info.best_friend_name = request.POST.get("best_friend_name", "")
        user_info.best_friend_contact_number = request.POST.get(
            "best_friend_contact_number", ""
        )
        user_info.save()
        return HttpResponse(
            "<h1>Congratulations: "
            + request.POST.get("full_name", "")
            + " your data have been saved successfully</h1>"
        )


def generate_qr_code(request):
    unique_id = uuid.uuid4().hex
    qr_code_name = "http://127.0.0.1:8000/get_qr_code_details/" + unique_id
    user_info = UserInfo()
    user_info.qr_code_number = unique_id
    user_info.save(name=qr_code_name)
    return redirect("view_all_details/")


def view_all_details(request):
    users_info = UserInfo.objects.all()
    return render(request, "view_all_User_details.html", {"users_info": users_info})


def get_login_page(request):
    return render(request, "login.html")


def post_login_page(request):
    email = request.POST.get("email", "")
    try:
        user_info = UserInfo.objects.filter(email=email).first()
        if user_info.password == request.POST.get("password", ""):
            return render(request, "edit_user_details.html", {"user_info": user_info})
        return render(
            request, "login.html", {"error": "Please enter valid email and password"}
        )
    except:
        return render(
            request, "login.html", {"error": "Please enter valid email and password"}
        )


def get_forgot_email(request):
    return render(request, "forgot_email.html")


def forgot_password(request):
    email = request.POST.get("email", "")
    try:
        user_info = UserInfo.objects.filter(email=email).first()
        if user_info:
            password = "".join(random.choices(string.ascii_letters, k=9))
            user_info.password = password
            user_info.save()
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            message = """\
            Subject: Your New password

            Your new password is {} . Please Do not share with anyone""".format(
                password
            )
            server.login("shahmeet21.ms@gmail.com", "tbnlgpbfufnzhaiw")
            server.sendmail("shahmeet21.ms@gmail.com", email, message)
        return render(
            request,
            "login.html",
            {"message": "Check your registered mail for new password"},
        )
    except:
        return render(request, "login.html", {"error": "Please enter valid email"})

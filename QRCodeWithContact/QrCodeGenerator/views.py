import os
import random
import smtplib
import string
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import requests
from cryptography.fernet import Fernet
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import redirect, render
from PIL import Image

# Create your views here.
from .constants import (
    EMAIL_PASSWORD,
    SALT,
    SENDER_MAIL_ID,
    SMTP_PORT,
    SMTP_URL,
    SUBJECT_FOR_FORGOT_PASSWORD,
    URL_PATH, SUBJECT_ALERT_EMAIL,
EMAIL_TYPE_FORGOT_PW,EMAIL_TYPE_INFO
)
from .models import FinalPic, PetOwnerInfo, TravellerInfo, UserInfo

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_qr_code_details(request, qr_code_number):
    ip = get_ip_address(request)
    try:
        if qr_code_number.startswith("user"):
            user_info = UserInfo.objects.filter(qr_code_number=qr_code_number).first()
            if user_info.email:
                send_mail(user_info.email, SUBJECT_ALERT_EMAIL,EMAIL_TYPE_INFO,ip=ip )
                return render(
                    request, "view_user_details.html", {"user_info": user_info}
                )
            return render(request, "enter_user_details.html", {"user_info": user_info})
        elif qr_code_number.startswith("pet"):
            pet_owner_info = PetOwnerInfo.objects.filter(
                qr_code_number=qr_code_number
            ).first()
            if pet_owner_info.email:
                return render(
                    request,
                    "view_pet_details.html",
                    {"pet_owner_info": pet_owner_info},
                )
            return render(
                request, "enter_pet_details.html", {"pet_owner_info": pet_owner_info}
            )
        else:
            traveller_info = TravellerInfo.objects.filter(
                qr_code_number=qr_code_number
            ).first()
            if traveller_info.email:
                return render(
                    request,
                    "view_traveller_details.html",
                    {"traveller_info": traveller_info},
                )
            return render(
                request,
                "enter_traveller_details.html",
                {"traveller_info": traveller_info},
            )

    except:
        return render(request, "enter_user_details.html", {"user_info": user_info})


def edit_save_user_details(request, id):
    return save_details_in_model(request, id)


def save_user_details(request, id):
    try:
        email = request.POST.get("email", "")
        user_info = UserInfo.objects.filter(email=email).first()
        if user_info:
            user_info = UserInfo.objects.get(id=id)
            return render(
                request,
                "enter_user_details.html",
                {
                    "error ": email
                    + " is already present please use different Email ID",
                    "user_info": user_info,
                },
            )
        else:
            return save_details_in_model(request, id)
    except:
        return save_details_in_model(request, id)


def save_details_in_model(request, id):
    fernet_key = Fernet(SALT)
    user_info = UserInfo.objects.get(id=id)
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
    return HttpResponse(
        "<h1>Congratulations: "
        + request.POST.get("full_name", "")
        + " your data have been saved successfully</h1>"
    )


def generate_qr_code(request):
    if request.POST.get("user", ""):
        generate_a4("user")
    elif request.POST.get("pet", ""):
        generate_a4("pet")
    else:
        generate_a4("traveller")

    return redirect("view_all_details/")


def generate_a4(type):
    script_directory = (
        os.path.dirname(os.path.abspath(__file__))[:-15] + "media\\documents\\"
    )
    final_image_paths = []
    for i in range(1, 89):
        unique_id = uuid.uuid4().hex
        file_name = f"qr_code_for_{type}_{unique_id}.png"
        image_path = script_directory + type + "\\" + file_name
        qr_code_name = URL_PATH + type + unique_id
        if type == "user":
            user_info = UserInfo()
            user_info.qr_code_number = type + unique_id
            user_info.save(name=qr_code_name, fname=file_name)
            final_image_paths.append(image_path)
        elif type == "traveller":
            traveller_info = TravellerInfo()
            traveller_info.qr_code_number = type + unique_id
            traveller_info.save(name=qr_code_name, fname=file_name)
            final_image_paths.append(image_path)
        else:
            pet_owner_info = PetOwnerInfo()
            pet_owner_info.qr_code_number = type + unique_id
            pet_owner_info.save(name=qr_code_name, fname=file_name)
            final_image_paths.append(image_path)

    cols = 8
    rows = 11
    # Calculate the size of each image in pixels to fit 2.5 cm on A4 paper
    image_size = int(2.5 * 300 / 2.54)  # 2.5 cm converted to pixels at 300 DPI

    # Create a new blank image for the collage
    collage_width = cols * image_size
    collage_height = rows * image_size
    collage = Image.new("RGB", (collage_width, collage_height))
    for i, img_path in enumerate(final_image_paths):
        img = Image.open(img_path)
        img = img.resize((image_size, image_size))

        row = i // cols
        col = i % cols
        x_offset = col * image_size
        y_offset = row * image_size

        collage.paste(img, (x_offset, y_offset))

    # Save the final collage

    fname = f"qr_code_for_{type}.png"
    final_pic = FinalPic()
    buffer = BytesIO()
    collage.save(buffer, "png")
    final_pic.image_name.save(fname, File(buffer), save=False)
    final_pic.type_of_image = type
    final_pic.save()
    collage.close()
    for image in final_image_paths:
        # Delete the file
        try:
            os.remove(image)
            print(f"{image} has been deleted.")
        except OSError as e:
            print(f"Error: {e} - {image} was not deleted.")


def view_all_details(request):
    final_pic = FinalPic.objects.order_by("-date_time").all()
    return render(request, "view_all_details.html", {"final_pic": final_pic})


def get_login_page(request):
    return render(request, "login.html")


def post_login_page(request):
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
            request, "login.html", {"error": "Please enter valid email and password"}
        )
    except Exception as e:
        print("Decryption failed:", e)
        return render(
            request, "login.html", {"error": "Please enter valid email and password"}
        )


def get_forgot_email(request):
    return render(request, "forgot_email.html")


def forgot_password(request):
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
                "forgot_password",
                password=password,
            )
            return render(
                request,
                "login.html",
                {"message": "Check your registered mail for new password"},
            )
    except:
        return render(request, "login.html", {"error": "Please enter valid email"})


def agrrement(request):
    return render(request, "agrrement.html")


def generate_msg_for_forgot_password(msg, password):
    # Create an HTML version of the message with bold text
    html_text = f"<html><body><p>Your new password for Sarathi is <strong>{password} </strong>. Please do not share it with anyone.</p></body></html>"

    part2 = MIMEText(html_text, "html")
    msg.attach(part2)
    return msg

def generate_msg_for_iquirer_detail(msg, gps_location, gps_url):
    # Create an HTML version of the message with bold text
    html_text = f"""<html><body><p>Someone scan your QR code. From this location <strong> {gps_location} </strong> . .</p>
         <a href={gps_url} >Check its GPS Location</a>
         </body></html>"""

    msg.attach(MIMEText(html_text, "html"))
    return msg





def send_mail(recipient_email, subject, type=None, password=None, ip=None):
    try:
        # Set up the MIMEText objects for the plain text and HTML parts
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SENDER_MAIL_ID
        msg["To"] = recipient_email
        if type == EMAIL_TYPE_FORGOT_PW:
            message = generate_msg_for_forgot_password(msg, password)
        if type == EMAIL_TYPE_INFO:
            gps_location, gps_url = get_details_from_ip("103.85.8.84")
            message = generate_msg_for_iquirer_detail(msg, gps_location,gps_url)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(SMTP_URL, SMTP_PORT) as server:
            server.login(SENDER_MAIL_ID, EMAIL_PASSWORD)
            server.sendmail(SENDER_MAIL_ID, recipient_email,message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print("Error:", e)


def get_details_from_ip(ip_address):
    latitude, longitude = get_lat_lon_from_ip(ip_address)
    gps_location = get_gps_location(latitude, longitude)
    gps_url = get_gps_url(latitude, longitude)
    return gps_location, gps_url
def get_lat_lon_from_ip(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json"

    response = requests.get(url)
    data = response.json()

    if "loc" in data:
        lat, lon = data["loc"].split(",")
        return lat, lon
    else:
        return None, None

def get_gps_location(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"

    response = requests.get(url)
    data = response.json()

    if 'display_name' in data:
        formatted_address = data['display_name']
        return formatted_address
    else:
        return None

def get_gps_url(latitude, longitude):
    base_url = "https://www.openstreetmap.org/?mlat={}&mlon={}&zoom=14"
    return base_url.format(latitude, longitude)
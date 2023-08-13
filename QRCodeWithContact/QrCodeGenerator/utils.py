import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from .constants import (EMAIL_PASSWORD, EMAIL_TYPE_FORGOT_PW, EMAIL_TYPE_INFO,
                        SENDER_MAIL_ID, SMTP_PORT, SMTP_URL)


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
            print(ip)
            gps_location, gps_url = get_details_from_ip(ip)
            message = generate_msg_for_iquirer_detail(msg, gps_location, gps_url)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(SMTP_URL, SMTP_PORT) as server:
            server.login(SENDER_MAIL_ID, EMAIL_PASSWORD)
            server.sendmail(SENDER_MAIL_ID, recipient_email, message.as_string())
        print("Email sent successfully. ", recipient_email)
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

    if "display_name" in data:
        formatted_address = data["display_name"]
        return formatted_address
    else:
        return None


def get_gps_url(latitude, longitude):
    base_url = "https://www.openstreetmap.org/?mlat={}&mlon={}&zoom=14"
    return base_url.format(latitude, longitude)


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


def get_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

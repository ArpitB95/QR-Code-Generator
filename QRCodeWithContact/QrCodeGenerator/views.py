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
from django.views.decorators.cache import never_cache
from PIL import Image

# Create your views here.
from .constants import (CONGRATULATION_MESSAGE, EMAIL_PASSWORD,
                        EMAIL_TYPE_FORGOT_PW, EMAIL_TYPE_INFO, SALT,
                        SENDER_MAIL_ID, SMTP_PORT, SMTP_URL,
                        SUBJECT_ALERT_EMAIL, SUBJECT_FOR_FORGOT_PASSWORD,
                        URL_PATH)
from .models import FinalPic, PetOwnerInfo, TravellerInfo, UserInfo

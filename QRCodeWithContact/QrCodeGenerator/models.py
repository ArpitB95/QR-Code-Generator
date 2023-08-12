from io import BytesIO

import qrcode
from django.core.files import File
from django.db import models
from PIL import Image, ImageDraw


# Create your models here.
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    qr_code_number = models.TextField(unique=True, blank=False)
    full_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=12)
    address = models.TextField()
    mother_name = models.CharField(max_length=22)
    mother_contact_number = models.CharField(max_length=12)
    father_name = models.CharField(max_length=20)
    father_contact_number = models.CharField(max_length=12)
    wife_name = models.CharField(max_length=20)
    wife_contact_number = models.CharField(max_length=12)
    husband_name = models.CharField(max_length=20)
    husband_contact_number = models.CharField(max_length=12)
    education_institute = models.CharField(max_length=20)
    education_institute_contact = models.CharField(max_length=12)
    work_place_name = models.CharField(max_length=30)
    work_place_address = models.TextField()
    work_place_contact_number = models.CharField(max_length=12)
    best_friend_name = models.CharField(max_length=20)
    best_friend_contact_number = models.CharField(max_length=12)
    qr_code = models.ImageField(upload_to="documents/user", blank=True)
    email = models.CharField(max_length=30, blank=True)
    password = models.TextField(blank=True)
    google_location_link = models.TextField(blank=True)
    children_name = models.CharField(max_length=20, blank=True)
    children_number = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return str(self.full_name)

    def save(self, *args, **kwargs):
        if kwargs.get("name"):
            name = str(kwargs["name"])
            fname = str(kwargs["fname"])
            qr = qrcode.QRCode(
                version=1,  # Automatically determine the version based on data
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,  # Adjust box size to control the overall size of the QR code
                border=4,  # Add a border around the QR code
            )
            qr.add_data(name)
            qr.make(fit=True)
            qr_code_image = qr.make_image(fill_color="black", back_color="white")
            qr_code_image = qr_code_image.resize((180, 180))
            canvas = Image.new("RGB", (185, 185), "white")
            ImageDraw.Draw(canvas)
            canvas.paste(qr_code_image)
            buffer = BytesIO()
            canvas.save(buffer, "PNG")
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save()


class TravellerInfo(models.Model):
    id = models.AutoField(primary_key=True)
    qr_code_number = models.TextField(unique=True, blank=False)
    full_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=12)
    current_country = models.CharField(max_length=25)
    current_address = models.TextField()
    current_location_link = models.TextField()
    destination_country = models.CharField(max_length=25)
    destination_address = models.TextField(blank=True)
    destination_location_link = models.TextField()
    email = models.CharField(blank=True, max_length=25)
    password = models.TextField(blank=True)
    qr_code = models.ImageField(upload_to="documents/traveller", blank=True)

    def __str__(self):
        return str(self.full_name)

    def save(self, *args, **kwargs):
        if kwargs.get("name"):
            name = str(kwargs["name"])
            fname = str(kwargs["fname"])
            qr = qrcode.QRCode(
                version=1,  # Automatically determine the version based on data
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,  # Adjust box size to control the overall size of the QR code
                border=4,  # Add a border around the QR code
            )
            qr.add_data(name)
            qr.make(fit=True)
            qr_code_image = qr.make_image(fill_color="black", back_color="white")
            qr_code_image = qr_code_image.resize((180, 180))
            canvas = Image.new("RGB", (185, 185), "white")
            ImageDraw.Draw(canvas)
            canvas.paste(qr_code_image)
            buffer = BytesIO()
            canvas.save(buffer, "PNG")
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save()


class PetOwnerInfo(models.Model):
    id = models.AutoField(primary_key=True)
    qr_code_number = models.TextField(unique=True, blank=False)
    pet_name = models.CharField(max_length=30)
    owner_full_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=12)
    address = models.TextField()
    current_location_link = models.TextField()
    zip_code = models.CharField(max_length=20)
    qr_code = models.ImageField(upload_to="documents/pet", blank=True)
    email = models.CharField(blank=True, max_length=25)
    password = models.TextField(blank=True)

    def __str__(self):
        return str(self.owner_full_name)

    def save(self, *args, **kwargs):
        if kwargs.get("name"):
            name = str(kwargs["name"])
            fname = str(kwargs["fname"])
            qr = qrcode.QRCode(
                version=1,  # Automatically determine the version based on data
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,  # Adjust box size to control the overall size of the QR code
                border=4,  # Add a border around the QR code
            )
            qr.add_data(name)
            qr.make(fit=True)
            qr_code_image = qr.make_image(fill_color="black", back_color="white")
            qr_code_image = qr_code_image.resize((180, 180))
            canvas = Image.new("RGB", (185, 185), "white")
            ImageDraw.Draw(canvas)
            canvas.paste(qr_code_image)
            buffer = BytesIO()
            canvas.save(buffer, "PNG")
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save()


class FinalPic(models.Model):
    id = models.AutoField(primary_key=True)
    image_name = models.ImageField(upload_to="documents/collage", blank=True)
    type_of_image = models.CharField(max_length=20, blank=True)
    date_time = models.DateTimeField(auto_now=True)

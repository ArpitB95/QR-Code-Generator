from django.db import models
from PIL import Image, ImageDraw
from io import BytesIO

import qrcode
from django.core.files import File


# Create your models here.
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    qr_code_number = models.TextField(unique=True, blank=False)
    full_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=12)
    address = models.TextField()
    mother_name = models.CharField(max_length=20)
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
    qr_code = models.ImageField(upload_to="documents/", blank=True)
    email = models.CharField(max_length=30, blank=True)
    password = models.TextField(blank=True)
    google_location_link = models.TextField(blank=True)
    children_name = models.CharField(max_length=20, blank=True)
    children_number = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return str(self.full_name)

    def save(self, *args, **kwargs):
        if kwargs.get("name"):
            id = kwargs.get("id")
            name = str(kwargs["name"])
            qr_code_image = qrcode.make(name)
            canvas = Image.new("RGB", (1000, 1000), "white")
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qr_code_image)
            fname = f"qr_code_for_{id}.png"
            buffer = BytesIO()
            canvas.save(buffer, "PNG")
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save()

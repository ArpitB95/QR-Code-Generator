# Generated by Django 4.2.4 on 2023-08-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FinalPic",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "image_name",
                    models.ImageField(blank=True, upload_to="documents/collage"),
                ),
                ("type_of_image", models.CharField(blank=True, max_length=20)),
                ("date_time", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PetOwnerInfo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("qr_code_number", models.TextField(unique=True)),
                ("pet_name", models.CharField(max_length=30)),
                ("owner_full_name", models.CharField(max_length=50)),
                ("contact_number", models.CharField(max_length=12)),
                ("address", models.TextField()),
                ("current_location_link", models.TextField()),
                ("zip_code", models.CharField(max_length=20)),
                ("qr_code", models.ImageField(blank=True, upload_to="documents/pet")),
                ("email", models.CharField(blank=True, max_length=25)),
                ("password", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="TravellerInfo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("qr_code_number", models.TextField(unique=True)),
                ("full_name", models.CharField(max_length=50)),
                ("contact_number", models.CharField(max_length=12)),
                ("current_country", models.CharField(max_length=25)),
                ("current_address", models.TextField()),
                ("current_location_link", models.TextField()),
                ("destination_country", models.CharField(max_length=25)),
                ("destination_address", models.TextField(blank=True)),
                ("destination_location_link", models.TextField()),
                ("email", models.CharField(blank=True, max_length=25)),
                ("password", models.TextField(blank=True)),
                (
                    "qr_code",
                    models.ImageField(blank=True, upload_to="documents/traveller"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("qr_code_number", models.TextField(unique=True)),
                ("full_name", models.CharField(max_length=50)),
                ("contact_number", models.CharField(max_length=12)),
                ("address", models.TextField()),
                ("mother_name", models.CharField(max_length=22)),
                ("mother_contact_number", models.CharField(max_length=12)),
                ("father_name", models.CharField(max_length=20)),
                ("father_contact_number", models.CharField(max_length=12)),
                ("wife_name", models.CharField(max_length=20)),
                ("wife_contact_number", models.CharField(max_length=12)),
                ("husband_name", models.CharField(max_length=20)),
                ("husband_contact_number", models.CharField(max_length=12)),
                ("education_institute", models.CharField(max_length=20)),
                ("education_institute_contact", models.CharField(max_length=12)),
                ("work_place_name", models.CharField(max_length=30)),
                ("work_place_address", models.TextField()),
                ("work_place_contact_number", models.CharField(max_length=12)),
                ("best_friend_name", models.CharField(max_length=20)),
                ("best_friend_contact_number", models.CharField(max_length=12)),
                ("qr_code", models.ImageField(blank=True, upload_to="documents/user")),
                ("email", models.CharField(blank=True, max_length=30)),
                ("password", models.TextField(blank=True)),
                ("google_location_link", models.TextField(blank=True)),
                ("children_name", models.CharField(blank=True, max_length=20)),
                ("children_number", models.CharField(blank=True, max_length=12)),
            ],
        ),
    ]

import os
import uuid
from io import BytesIO

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from PIL import Image

from .constants import URL_PATH
from .models import FinalPic, PetOwnerInfo, TravellerInfo, UserInfo


@login_required
def view_all_details(request):
    final_pic = FinalPic.objects.order_by("-date_time").all()
    return render(request, "view_all_details.html", {"final_pic": final_pic})


@never_cache
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
        except OSError as e:
            print(f"Error: {e} - {image} was not deleted.")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login page
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("view_all_details")
    return render(request, "login.html")

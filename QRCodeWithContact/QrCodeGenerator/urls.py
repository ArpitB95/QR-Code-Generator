from django.urls import path

from .common import agrrement, get_qr_code_details
from .pet_view import (forgot_pet_password, get_forgot_pet_email,
                       get_pet_login_page, post_login_pet_page,
                       save_edited_pet_details, save_pet_details)
from .super_user import generate_qr_code, view_all_details
from .traveller_view import (forgot_traveller_password,
                             get_forgot_traveller_email,
                             get_traveller_login_page,
                             post_login_traveller_page,
                             save_edited_traveller_details,
                             save_traveller_details)
from .user_view import (forgot_user_password, get_forgot_user_email,
                        get_user_login_page, post_login_user_page,
                        save_edited_user_details, save_user_details)

urlpatterns = [
    path("forgot_user_password", forgot_user_password, name="forgot_user_password"),
    path("forgot_pet_password", forgot_pet_password, name="forgot_pet_password"),
    path(
        "forgot_traveller_password",
        forgot_traveller_password,
        name="forgot_traveller_password",
    ),
    path("get_forgot_user_email/", get_forgot_user_email, name="get_forgot_user_email"),
    path("get_forgot_pet_email/", get_forgot_pet_email, name="get_forgot_pet_email"),
    path(
        "get_forgot_traveller_email/",
        get_forgot_traveller_email,
        name="get_forgot_traveller_email",
    ),
    path("get_user_login_page/", get_user_login_page, name="get_user_login_page"),
    path("get_pet_login_page/", get_pet_login_page, name="get_pet_login_page"),
    path(
        "get_traveller_login_page/",
        get_traveller_login_page,
        name="get_traveller_login_page",
    ),
    path("post_login_user_page", post_login_user_page, name="post_login_user_page"),
    path("post_login_pet_page", post_login_pet_page, name="post_login_pet_page"),
    path(
        "post_login_traveller_page",
        post_login_traveller_page,
        name="post_login_traveller_page",
    ),
    path(
        "save_edited_user_details/<str:qr_code_number>",
        save_edited_user_details,
        name="save_edited_user_details",
    ),
    path(
        "save_edited_pet_details/<str:qr_code_number>",
        save_edited_pet_details,
        name="save_edited_pet_details",
    ),
    path(
        "save_edited_traveller_details/<str:qr_code_number>",
        save_edited_traveller_details,
        name="save_edited_traveller_details",
    ),
    path(
        "save_user_details/<str:qr_code_number>",
        save_user_details,
        name="save_user_details",
    ),
    path(
        "save_pet_details/<str:qr_code_number>",
        save_pet_details,
        name="save_pet_details",
    ),
    path(
        "save_traveller_details/<str:qr_code_number>",
        save_traveller_details,
        name="save_traveller_details",
    ),
    path("view_all_details/", view_all_details, name="view_all_details"),
    path(
        "get_qr_code_details/<str:qr_code_number>",
        get_qr_code_details,
        name="get_qr_code_details",
    ),
    path("generate_qr_code", generate_qr_code, name="generate_qr_code"),
    path("agrrement/", agrrement, name="agrrement"),
]

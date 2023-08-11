from django.urls import path

from .views import (
    agrrement,
    edit_save_user_details,
    forgot_password,
    generate_qr_code,
    get_forgot_email,
    get_login_page,
    get_qr_code_details,
    post_login_page,
    save_user_details,
    view_all_details,
)

urlpatterns = [
    path("view_all_details/", view_all_details, name="view_all_details"),
    path(
        "get_qr_code_details/<str:qr_code_number>",
        get_qr_code_details,
        name="get_qr_code_details",
    ),
    path("generate_qr_code", generate_qr_code, name="generate_qr_code"),
    path(
        "save_user_details/<int:id>",
        save_user_details,
        name="save_user_details",
    ),
    path(
        "edit_save_user_details/<int:id>",
        edit_save_user_details,
        name="edit_save_user_details",
    ),
    path("login/", get_login_page, name="login"),
    path("post_login_page", post_login_page, name="post_login_page"),
    path("forgot_password", forgot_password, name="forgot_password"),
    path("get_forgot_email/", get_forgot_email, name="get_forgot_email"),
    path("agrrement/", agrrement, name="get_forgot_email"),
]

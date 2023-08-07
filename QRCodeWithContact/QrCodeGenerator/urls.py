from django.urls import path

from .views import (
    view_all_details,
    get_qr_code_details,
    generate_qr_code,
    save_user_details,
    get_login_page,
    post_login_page,
    forgot_password,
    get_forgot_email,
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
        "save_user_details/<str:qr_code_number>",
        save_user_details,
        name="save_user_details",
    ),
    path("login/", get_login_page, name="login"),
    path("post_login_page", post_login_page, name="post_login_page"),
    path("forgot_password", forgot_password, name="forgot_password"),
    path("get_forgot_email/", get_forgot_email, name="get_forgot_email"),
]

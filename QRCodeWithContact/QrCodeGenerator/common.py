from django.shortcuts import render
from django.views.decorators.cache import never_cache

# Create your views here.
from .constants import EMAIL_TYPE_INFO, SUBJECT_ALERT_EMAIL
from .models import PetOwnerInfo, TravellerInfo, UserInfo
from .utils import get_ip_address, send_mail


@never_cache
def get_qr_code_details(request, qr_code_number):
    ip = get_ip_address(request)
    try:
        if qr_code_number.startswith("user"):
            user_info = UserInfo.objects.filter(qr_code_number=qr_code_number).first()
            if user_info.email:
                send_mail(user_info.email, SUBJECT_ALERT_EMAIL, EMAIL_TYPE_INFO, ip=ip)
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


def agrrement(request):
    return render(request, "agrrement.html")

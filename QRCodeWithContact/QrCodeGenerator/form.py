from django import forms
from .models import UserInfo


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            "full_name",
            "contact_number",
            "address",
            "mother_name",
            "mother_contact_number",
            "father_name",
            "father_contact_number",
            "wife_name",
            "wife_contact_number",
            "husband_name",
            "husband_contact_number",
            "education_institute",
            "education_institute_contact",
            "work_place_name",
            "work_place_address",
            "work_place_contact_number",
            "best_friend_name",
            "best_friend_contact_number",
        ]

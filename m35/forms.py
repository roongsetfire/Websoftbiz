# forms.py
from django import forms
from django.utils import timezone
from .models import CmtRctr

class CmtRctrForm(forms.ModelForm):
    class Meta:
        model = CmtRctr
        fields = [
            "r_c_no",
            "date",
            "payin",
            "room_no_1",
            "room_no_2",
            "member_1",
            "member_2",
            "type",
            "payment_method",
            "bank_1",
            "bank_2",
            "bank_no",
            "bank_date",
            "vat",
            "deduct_from_prepaid",
            "withdraw_from_bankaccount",
            "withdraw",
            "total",
            "tax_no",
            "tax_date",
            "no_ref",
            "remark_1",
            "remark_2",
            "textstamp",
            # "timestamp",
        ]
# forms.py
from django import forms
from django.utils import timezone
from .models import CmtArtr, CmtArtrItem


class CmtArtrForm(forms.ModelForm):
    class Meta:
        model = CmtArtr
        fields = [
            "bill_no",
            "date",
            "month",
            "year",
            "prd",
            "room_no_1",
            "room_no_2",
            "member_1",
            "member_2",
            "duedate",
            "remark_1",
            "textstamp",
        ]

        widgets = {
            "bill_no": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "เลขที่ใบเสร็จ"}
            ),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "month": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "เดือน"}
            ),
            "year": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ปี"}
            ),
            "prd": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "งวด'"}
            ),
            "room_no_1": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "เลขห้องที่ 1"}
            ),
            "room_no_2": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "เลขห้องที่ 2"}
            ),
            "member_1": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "รหัส-ชื่อ 1"}
            ),
            "member_2": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "รหัส-ชื่อ 2"}
            ),
            "duedate": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "remark_1": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ชำระภายในวันที่"}
            ),
            "textstamp": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "หมายเหตุ"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # กำหนดค่าเริ่มต้น
        if not self.instance.pk:  # ถ้าเป็นการสร้างใหม่
            today = timezone.now().date()
            self.fields["date"].initial = today
            self.fields["year"].initial = str(today.year)
            self.fields["month"].initial = str(today.month).zfill(2)


class CmtArtrItemForm(forms.ModelForm):
    class Meta:
        model = CmtArtrItem
        fields = [
            "row_number",
            "item_code",
            "description",
            "rate",
            "quantity",
            "amount",
        ]

        widgets = {
            "row_number": forms.NumberInput(attrs={"class": "form-control"}),
            "item_code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "rate": forms.NumberInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

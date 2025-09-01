# forms.py
from django import forms
from django.utils import timezone
from .models import CmtArtr, CmtArtrItem


class CmtArtrForm(forms.ModelForm):
    class Meta:
        model = CmtArtr
        fields = "__all__"  # หรือระบุฟิลด์ที่ต้องการ

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
                attrs={"class": "form-control", "placeholder": "หมายเหตุ 1"}
            ),
            "remark_2": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "หมายเหตุ 2"}
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
            "room_no",
            "m_y_prd",
            "bill_no",
            "item_code",
            "description",
            "rate",
            "quantity",
            "amount",
        ]

        widgets = {
            "room_no": forms.TextInput(attrs={"class": "form-control"}),
            "m_y_prd": forms.TextInput(attrs={"class": "form-control"}),
            "bill_no": forms.TextInput(attrs={"class": "form-control"}),
            "item_code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "rate": forms.NumberInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

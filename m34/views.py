from django.shortcuts import render
from .models import CmtArtr, CmtArtrItem
from .forms import CmtArtrForm
from django.contrib import messages
import json


def m34(request):
    """หน้าแสดงรายการข้อมูลใบเสร็จ"""
    cmt_artr = CmtArtr.objects.all()
    cmt_artr_item = CmtArtrItem.objects.all()

    if request.method == "POST":
        form = CmtArtrForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "เพิ่มสินค้าเรียบร้อยแล้ว!")
        else:
            messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    else:
        form = CmtArtrForm()

    # Build dictionary for JavaScript auto-fill
    item_dict = {
        item.item_code: {
            "description": item.description,
            "rate": float(item.rate),
            "quantity": float(item.quantity),
            "amount": float(item.amount),
        }
        for item in cmt_artr_item
        if item.item_code
    }

    context = {
        "form": form,
        "cmt_artr": cmt_artr,
        "cmt_artr_item": cmt_artr_item,
        "item_data_json": json.dumps(item_dict),  # pass to template
        "f_12": "F2 เพิ่ม",
    }
    return render(request, "m34/index.html", context)

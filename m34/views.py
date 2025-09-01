# from django.shortcuts import render
# from .models import CmtArtr, CmtArtrItem
# from .forms import CmtArtrForm
# from django.contrib import messages
# import json


# def m34(request):
#     """หน้าแสดงรายการข้อมูลใบเสร็จ"""
#     cmt_artr = CmtArtr.objects.all()
#     cmt_artr_item = CmtArtrItem.objects.all()

#     if request.method == "POST":
#         form = CmtArtrForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "เพิ่มสินค้าเรียบร้อยแล้ว!")
#         else:
#             messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
#     else:
#         form = CmtArtrForm()

#     # Build dictionary for JavaScript auto-fill
#     item_dict = {
#         item.item_code: {
#             "description": item.description,
#             "rate": float(item.rate),
#             "quantity": float(item.quantity),
#             "amount": float(item.amount),
#         }
#         for item in cmt_artr_item
#         if item.item_code
#     }

#     context = {
#         "form": form,
#         "cmt_artr": cmt_artr,
#         "cmt_artr_item": cmt_artr_item,
#         "item_data_json": json.dumps(item_dict),  # pass to template
#         "f_12": "F2 เพิ่ม",
#     }
#     return render(request, "m34/index.html", context)
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import CmtArtr, CmtArtrItem
from .forms import CmtArtrForm
from django.contrib import messages
import json
from django.core.paginator import Paginator
from django.db.models import Max
import datetime


def generate_bill_no():
    """สร้างเลขที่ใบแจ้งหนี้อัตโนมัติ"""
    today = datetime.date.today()
    prefix = today.strftime("%Y%m%d")  # YYYYMMDD

    # หาเลขที่สูงสุดของวันนี้
    latest = CmtArtr.objects.filter(bill_no__startswith=prefix).aggregate(
        max_no=Max("bill_no")
    )

    if latest["max_no"]:
        # ดึงเลขท้าย 3 หลัก แล้วบวก 1
        last_num = int(latest["max_no"][-3:])
        new_num = last_num + 1
    else:
        new_num = 1

    return f"{prefix}-{new_num:03d}"  # format: 20231201-001


def m34(request):
    """หน้าแสดงรายการข้อมูลใบเสร็จ"""

    # ถ้าเป็น GET request สำหรับขอเลขที่ใหม่
    if request.method == "GET" and request.GET.get("action") == "get_new_bill_no":
        new_bill_no = generate_bill_no()
        return JsonResponse({"status": "success", "bill_no": new_bill_no})

    # เพิ่มใน function m34() ก่อน POST request
    if request.method == "GET" and request.GET.get("action") == "get_record":
        record_id = request.GET.get("id")
        try:
            record = CmtArtr.objects.get(id=record_id)

            # ดึงข้อมูล items ที่เกี่ยวข้อง
            items = CmtArtrItem.objects.filter(
                bill_no=record.bill_no
            ).first()  # ดึงรายการแรก

            return JsonResponse(
                {
                    "status": "success",
                    "record": {
                        "bill_no": record.bill_no,
                        "date": record.date.strftime("%Y-%m-%d") if record.date else "",
                        "month": record.month,
                        "year": record.year,
                        "prd": record.prd,  # ดึง prd จาก database
                        "room_no_1": record.room_no_1,
                        "room_no_2": record.room_no_2,
                        "member_1": record.member_1,  # ดึง member_1 จาก database
                        "member_2": record.member_2,
                        "duedate": (
                            record.duedate.strftime("%Y-%m-%d")
                            if record.duedate
                            else ""
                        ),
                        "remark_1": record.remark_1,
                        "remark_2": record.remark_2,
                        # ข้อมูล Item (ถ้ามี)
                        "item_code": items.item_code if items else "",
                        "description": items.description if items else "",
                        "rate": str(items.rate) if items else "",
                        "quantity": str(items.quantity) if items else "",
                        "amount": str(items.amount) if items else "",
                    },
                }
            )
        except CmtArtr.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Record not found"})

    # ถ้าเป็น AJAX POST request
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        try:
            action = request.POST.get("action")

            if action == "create":
                # ตรวจสอบเลขที่ใบแจ้งหนี้ซ้ำ
                bill_no = request.POST.get("bill_no")
                if CmtArtr.objects.filter(bill_no=bill_no).exists():
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": f"เลขที่ใบแจ้งหนี้ {bill_no} มีอยู่แล้ว กรุณาใช้เลขที่อื่น",
                        }
                    )

                # สร้างข้อมูลใหม่
                artr = CmtArtr()
                artr.bill_no = bill_no
                artr.date = request.POST.get("date")
                artr.month = request.POST.get("month")
                artr.year = request.POST.get("year")
                artr.prd = request.POST.get("prd")
                artr.room_no_1 = request.POST.get("room_no_1")
                artr.room_no_2 = request.POST.get("room_no_2")
                artr.member_1 = request.POST.get("member_1")
                artr.member_2 = request.POST.get("member_2")

                # จัดการ duedate - ถ้าไม่มีค่าให้ใช้วันที่ปัจจุบัน + 30 วัน
                duedate = request.POST.get("duedate")
                if not duedate or duedate.strip() == "":
                    # ใช้วันที่ปัจจุบัน + 30 วัน
                    artr.duedate = datetime.date.today() + datetime.timedelta(days=30)
                else:
                    artr.duedate = duedate

                artr.remark_1 = request.POST.get("remark_1")
                artr.remark_2 = request.POST.get("remark_2")
                artr.save()

                # สร้าง item ถ้ามี
                if request.POST.get("item_code"):
                    item = CmtArtrItem()
                    item.artr = artr
                    item.item_code = request.POST.get("item_code")
                    item.description = request.POST.get("description")
                    item.rate = float(request.POST.get("rate") or 0)
                    item.quantity = float(request.POST.get("quantity") or 0)
                    item.amount = float(request.POST.get("amount") or 0)
                    item.save()

                return JsonResponse(
                    {"status": "success", "message": "เพิ่มข้อมูลเรียบร้อยแล้ว"}
                )

            elif action == "edit":
                # แก้ไขข้อมูล
                artr_id = request.POST.get("id")
                artr = CmtArtr.objects.get(id=artr_id)
                artr.bill_no = request.POST.get("bill_no")
                artr.date = request.POST.get("date")
                artr.month = request.POST.get("month")
                artr.year = request.POST.get("year")
                artr.prd = request.POST.get("prd")
                artr.room_no_1 = request.POST.get("room_no_1")
                artr.room_no_2 = request.POST.get("room_no_2")
                artr.member_1 = request.POST.get("member_1")
                artr.member_2 = request.POST.get("member_2")

                # จัดการ duedate
                duedate = request.POST.get("duedate")
                if not duedate or duedate.strip() == "":
                    # ใช้วันที่ปัจจุบัน + 30 วัน
                    artr.duedate = datetime.date.today() + datetime.timedelta(days=30)
                else:
                    artr.duedate = duedate

                artr.remark_1 = request.POST.get("remark_1")
                artr.remark_2 = request.POST.get("remark_2")
                artr.save()

                return JsonResponse(
                    {"status": "success", "message": "แก้ไขข้อมูลเรียบร้อยแล้ว"}
                )

            elif action == "delete":
                # ลบข้อมูล
                artr_id = request.POST.get("id")
                artr = CmtArtr.objects.get(id=artr_id)
                artr.delete()

                return JsonResponse(
                    {"status": "success", "message": "ลบข้อมูลเรียบร้อยแล้ว"}
                )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"เกิดข้อผิดพลาด: {str(e)}"}
            )

    # ถ้าเป็น GET request (แสดงหน้าปกติ)
    cmt_artr = CmtArtr.objects.all().order_by("-id")
    cmt_artr_item = CmtArtrItem.objects.all()

    # Pagination
    paginator = Paginator(cmt_artr, 10)  # 10 records per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        # Django form submit (ถ้าไม่ใช่ AJAX)
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
            "rate": float(item.rate) if item.rate else 0,
            "quantity": float(item.quantity) if item.quantity else 0,
            "amount": float(item.amount) if item.amount else 0,
        }
        for item in cmt_artr_item
        if item.item_code
    }

    context = {
        "form": form,
        "cmt_artr": page_obj,  # ใช้ page_obj แทน cmt_artr
        "page_obj": page_obj,
        "cmt_artr_item": cmt_artr_item,
        "item_data_json": json.dumps(item_dict),
        "f_12": "F2 เพิ่ม",
    }
    return render(request, "m34/index.html", context)

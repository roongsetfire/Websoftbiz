from django.shortcuts import render
from django.http import JsonResponse
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

    latest = CmtArtr.objects.filter(bill_no__startswith=prefix).aggregate(
        max_no=Max("bill_no")
    )

    if latest["max_no"]:
        last_num = int(latest["max_no"][-3:])
        new_num = last_num + 1
    else:
        new_num = 1

    return f"{prefix}-{new_num:03d}"


def m34(request):
    """หน้าแสดงรายการข้อมูลใบเสร็จ"""

    # ---------------- GET NEW BILL_NO ----------------
    if request.method == "GET" and request.GET.get("action") == "get_new_bill_no":
        new_bill_no = generate_bill_no()
        return JsonResponse({"status": "success", "bill_no": new_bill_no})

    # ---------------- GET RECORD ----------------
    if request.method == "GET" and request.GET.get("action") == "get_record":
        record_id = request.GET.get("id")
        try:
            record = CmtArtr.objects.get(id=record_id)
            items = list(CmtArtrItem.objects.filter(bill_no=record.bill_no).values())

            return JsonResponse(
                {
                    "status": "success",
                    "record": {
                        "bill_no": record.bill_no,
                        "date": record.date.strftime("%Y-%m-%d") if record.date else "",
                        "month": record.month,
                        "year": record.year,
                        "prd": record.prd,
                        "room_no_1": record.room_no_1,
                        "room_no_2": record.room_no_2,
                        "member_1": record.member_1,
                        "member_2": record.member_2,
                        "duedate": (
                            record.duedate.strftime("%Y-%m-%d")
                            if record.duedate
                            else ""
                        ),
                        "remark_1": record.remark_1,
                        "remark_2": record.remark_2,
                        "items": items,  # 👈 ส่งกลับทั้งหมด
                    },
                }
            )
        except CmtArtr.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Record not found"})

    # ---------------- DELETE ----------------
    if request.method == "POST" and request.POST.get("action") == "delete":
        record_id = request.POST.get("id")
        try:
            record = CmtArtr.objects.get(id=record_id)
            CmtArtrItem.objects.filter(bill_no=record.bill_no).delete()
            record.delete()
            return JsonResponse({"status": "success", "message": "ลบข้อมูลเรียบร้อยแล้ว"})
        except CmtArtr.DoesNotExist:
            return JsonResponse({"status": "error", "message": "ไม่พบข้อมูลที่ต้องการลบ"})
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"เกิดข้อผิดพลาด: {str(e)}"}
            )

    # ---------------- CREATE / EDIT ----------------
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        try:
            action = request.POST.get("action")

            # ---------- CREATE ----------
            if action == "create":
                bill_no = request.POST.get("bill_no")
                if CmtArtr.objects.filter(bill_no=bill_no).exists():
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": f"เลขที่ใบแจ้งหนี้ {bill_no} มีอยู่แล้ว",
                        }
                    )

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

                duedate = request.POST.get("duedate")
                if not duedate or duedate.strip() == "":
                    artr.duedate = datetime.date.today() + datetime.timedelta(days=30)
                else:
                    artr.duedate = duedate

                artr.remark_1 = request.POST.get("remark_1")
                artr.remark_2 = request.POST.get("remark_2")
                artr.save()

                # บันทึกรายการใหม่ทั้งหมด
                m_y_prd = f"{artr.month}/{artr.year}/{artr.prd}"
                item_codes = request.POST.getlist("item_code[]")
                descriptions = request.POST.getlist("description[]")
                rates = request.POST.getlist("rate[]")
                quantities = request.POST.getlist("quantity[]")
                amounts = request.POST.getlist("amount[]")

                for i in range(len(item_codes)):
                    if not item_codes[i].strip():
                        continue
                    item = CmtArtrItem()
                    item.bill_no = bill_no
                    item.room_no = request.POST.get("room_no_1")
                    item.m_y_prd = m_y_prd
                    item.item_code = item_codes[i]
                    item.description = descriptions[i]
                    item.rate = float(rates[i] or 0)
                    item.quantity = float(quantities[i] or 0)
                    item.amount = float(amounts[i] or 0)
                    item.save()

                return JsonResponse(
                    {"status": "success", "message": "เพิ่มข้อมูลเรียบร้อยแล้ว"}
                )

            # ---------- EDIT ----------
            elif action == "edit":
                artr_id = request.POST.get("id")
                artr = CmtArtr.objects.get(id=artr_id)
                bill_no = request.POST.get("bill_no")

                artr.bill_no = bill_no
                artr.date = request.POST.get("date")
                artr.month = request.POST.get("month")
                artr.year = request.POST.get("year")
                artr.prd = request.POST.get("prd")
                artr.room_no_1 = request.POST.get("room_no_1")
                artr.room_no_2 = request.POST.get("room_no_2")
                artr.member_1 = request.POST.get("member_1")
                artr.member_2 = request.POST.get("member_2")

                duedate = request.POST.get("duedate")
                if not duedate or duedate.strip() == "":
                    artr.duedate = datetime.date.today() + datetime.timedelta(days=30)
                else:
                    artr.duedate = duedate

                artr.remark_1 = request.POST.get("remark_1")
                artr.remark_2 = request.POST.get("remark_2")
                artr.save()

                # ✅ เพิ่มเฉพาะแถวใหม่ ไม่ลบของเก่า
                m_y_prd = f"{artr.month}/{artr.year}/{artr.prd}"
                item_codes = request.POST.getlist("item_code[]")
                descriptions = request.POST.getlist("description[]")
                rates = request.POST.getlist("rate[]")
                quantities = request.POST.getlist("quantity[]")
                amounts = request.POST.getlist("amount[]")

                for i in range(len(item_codes)):
                    if not item_codes[i].strip():
                        continue
                    # เช็คว่ามี item_code นี้แล้วหรือยัง (กัน duplicate)
                    if CmtArtrItem.objects.filter(
                        bill_no=bill_no, item_code=item_codes[i]
                    ).exists():
                        continue

                    item = CmtArtrItem()
                    item.bill_no = bill_no
                    item.room_no = request.POST.get("room_no_1")
                    item.m_y_prd = m_y_prd
                    item.item_code = item_codes[i]
                    item.description = descriptions[i]
                    item.rate = float(rates[i] or 0)
                    item.quantity = float(quantities[i] or 0)
                    item.amount = float(amounts[i] or 0)
                    item.save()

                return JsonResponse(
                    {"status": "success", "message": "แก้ไขข้อมูลเรียบร้อยแล้ว"}
                )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"เกิดข้อผิดพลาด: {str(e)}"}
            )

    # ---------------- GET PAGE ----------------
    cmt_artr = CmtArtr.objects.all().order_by("-id")
    cmt_artr_item = CmtArtrItem.objects.all()

    paginator = Paginator(cmt_artr, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = CmtArtrForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "เพิ่มสินค้าเรียบร้อยแล้ว!")
        else:
            messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    else:
        form = CmtArtrForm()

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
        "row_numbers": range(1, 9),
        "form": form,
        "cmt_artr": page_obj,
        "page_obj": page_obj,
        "cmt_artr_item": cmt_artr_item,
        "item_data_json": json.dumps(item_dict),
        "f_12": "F2 เพิ่ม",
    }
    return render(request, "m34/index.html", context)

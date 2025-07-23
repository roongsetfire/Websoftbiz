# from django.shortcuts import render
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.db.models import Q
# from django.http import JsonResponse
# from datetime import datetime, date
# from expense.models import CmtArtr
# from expense.forms import CmtArtrForm


# def m34(request):

#     """หน้าแสดงรายการข้อมูลใบเสร็จ"""
#     search_query = request.GET.get("search", "")
#     date_from = request.GET.get("date_from", "")
#     date_to = request.GET.get("date_to", "")

#     # Query ข้อมูล
#     queryset = CmtArtr.objects.all()

#     # ค้นหา
#     if search_query:
#         queryset = queryset.filter(
#             Q(bill_no__icontains=search_query)
#             | Q(member_1__icontains=search_query)
#             | Q(member_2__icontains=search_query)
#             | Q(prd__icontains=search_query)
#         )

#     # กรองตามวันที่
#     if date_from:
#         queryset = queryset.filter(date__gte=date_from)
#     if date_to:
#         queryset = queryset.filter(date__lte=date_to)

#     # Pagination
#     paginator = Paginator(queryset, 20)  # แสดง 20 รายการต่อหน้า
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = {
#         "page_obj": page_obj,
#         "search_query": search_query,
#         "date_from": date_from,
#         "date_to": date_to,
#         "total_records": queryset.count(),
#     }

#     return render(request, "m34/index.html", context)

# views.py
# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.core.paginator import Paginator
# from django.db.models import Q
# from django.db import transaction
# from django.contrib import messages
# import json
# from datetime import datetime, date
# from decimal import Decimal
# from expense.models import CmtArtr, CmtArtrItem


# def m34(request):
#     """หน้าแสดงรายการข้อมูลใบเสร็จ"""
#     search_query = request.GET.get("search", "")
#     date_from = request.GET.get("date_from", "")
#     date_to = request.GET.get("date_to", "")

#     # Query ข้อมูล
#     queryset = CmtArtr.objects.all()

#     # ค้นหา
#     if search_query:
#         queryset = queryset.filter(
#             Q(bill_no__icontains=search_query)
#             | Q(member_1__icontains=search_query)
#             | Q(member_2__icontains=search_query)
#             | Q(prd__icontains=search_query)
#         )

#     # กรองตามวันที่
#     if date_from:
#         queryset = queryset.filter(date__gte=date_from)
#     if date_to:
#         queryset = queryset.filter(date__lte=date_to)

#     # Pagination
#     paginator = Paginator(queryset, 20)  # แสดง 20 รายการต่อหน้า
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = {
#         "page_obj": page_obj,
#         "search_query": search_query,
#         "date_from": date_from,
#         "date_to": date_to,
#         "total_records": queryset.count(),
#     }

#     return render(request, "m34/index.html", context)


# @csrf_exempt
# @require_http_methods(["POST"])
# def create_bill(request):
#     """สร้างใบแจ้งหนี้ใหม่"""
#     try:
#         data = json.loads(request.body)

#         # ตรวจสอบข้อมูลที่จำเป็น
#         required_fields = ['bill_no', 'date', 'month', 'year', 'member_1', 'duedate']
#         for field in required_fields:
#             if not data.get(field):
#                 return JsonResponse({
#                     'success': False,
#                     'message': f'กรุณากรอก {field}'
#                 }, status=400)

#         # ตรวจสอบเลขที่ใบแจ้งหนี้ซ้ำ
#         if CmtArtr.objects.filter(bill_no=data['bill_no']).exists():
#             return JsonResponse({
#                 'success': False,
#                 'message': 'เลขที่ใบแจ้งหนี้นี้มีอยู่แล้ว'
#             }, status=400)

#         with transaction.atomic():
#             # สร้างใบแจ้งหนี้หลัก
#             bill = CmtArtr.objects.create(
#                 bill_no=data['bill_no'],
#                 date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
#                 month=data['month'],
#                 year=data['year'],
#                 prd=data.get('prd', ''),
#                 room_no_1=data.get('room_no_1', ''),
#                 room_no_2=data.get('room_no_2', ''),
#                 member_1=data['member_1'],
#                 member_2=data.get('member_2', ''),
#                 duedate=datetime.strptime(data['duedate'], '%Y-%m-%d').date(),
#                 remark_1=data.get('remark_1', ''),
#                 textstamp=data.get('textstamp', ''),
#                 paid_amount=Decimal(str(data.get('paid_amount', 0)))
#             )

#             # สร้างรายการสินค้า
#             for item_data in data.get('items', []):
#                 if (item_data.get('code') or item_data.get('description') or
#                     item_data.get('rate') or item_data.get('qty')):
#                     CmtArtrItem.objects.create(
#                         bill=bill,
#                         row_number=item_data['row'],
#                         item_code=item_data.get('code', ''),
#                         description=item_data.get('description', ''),
#                         rate=Decimal(str(item_data.get('rate', 0))),
#                         quantity=Decimal(str(item_data.get('qty', 0))),
#                         amount=Decimal(str(item_data.get('amount', 0)))
#                     )

#             # คำนวณยอดรวม
#             bill.calculate_totals()

#             return JsonResponse({
#                 'success': True,
#                 'message': 'บันทึกใบแจ้งหนี้เรียบร้อย',
#                 'bill_id': bill.id
#             })

#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'เกิดข้อผิดพลาด: {str(e)}'
#         }, status=500)


# @csrf_exempt
# @require_http_methods(["PUT"])
# def update_bill(request, bill_id):
#     """อัพเดทใบแจ้งหนี้"""
#     try:
#         bill = get_object_or_404(CmtArtr, id=bill_id)
#         data = json.loads(request.body)

#         # ตรวจสอบเลขที่ใบแจ้งหนี้ซ้ำ (ยกเว้นตัวเอง)
#         if (data.get('bill_no') != bill.bill_no and
#             CmtArtr.objects.filter(bill_no=data['bill_no']).exists()):
#             return JsonResponse({
#                 'success': False,
#                 'message': 'เลขที่ใบแจ้งหนี้นี้มีอยู่แล้ว'
#             }, status=400)

#         with transaction.atomic():
#             # อัพเดทข้อมูลหลัก
#             bill.bill_no = data['bill_no']
#             bill.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
#             bill.month = data['month']
#             bill.year = data['year']
#             bill.prd = data.get('prd', '')
#             bill.room_no_1 = data.get('room_no_1', '')
#             bill.room_no_2 = data.get('room_no_2', '')
#             bill.member_1 = data['member_1']
#             bill.member_2 = data.get('member_2', '')
#             bill.duedate = datetime.strptime(data['duedate'], '%Y-%m-%d').date()
#             bill.remark_1 = data.get('remark_1', '')
#             bill.textstamp = data.get('textstamp', '')
#             bill.paid_amount = Decimal(str(data.get('paid_amount', 0)))
#             bill.save()

#             # ลบรายการเก่าและสร้างใหม่
#             bill.bill_items.all().delete()

#             for item_data in data.get('items', []):
#                 if (item_data.get('code') or item_data.get('description') or
#                     item_data.get('rate') or item_data.get('qty')):
#                     CmtArtrItem.objects.create(
#                         bill=bill,
#                         row_number=item_data['row'],
#                         item_code=item_data.get('code', ''),
#                         description=item_data.get('description', ''),
#                         rate=Decimal(str(item_data.get('rate', 0))),
#                         quantity=Decimal(str(item_data.get('qty', 0))),
#                         amount=Decimal(str(item_data.get('amount', 0)))
#                     )

#             # คำนวณยอดรวม
#             bill.calculate_totals()

#             return JsonResponse({
#                 'success': True,
#                 'message': 'อัพเดทใบแจ้งหนี้เรียบร้อย'
#             })

#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'เกิดข้อผิดพลาด: {str(e)}'
#         }, status=500)


# @csrf_exempt
# @require_http_methods(["DELETE"])
# def delete_bill(request, bill_id):
#     """ลบใบแจ้งหนี้"""
#     try:
#         bill = get_object_or_404(CmtArtr, id=bill_id)
#         bill_no = bill.bill_no
#         bill.delete()

#         return JsonResponse({
#             'success': True,
#             'message': f'ลบใบแจ้งหนี้ {bill_no} เรียบร้อย'
#         })

#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'เกิดข้อผิดพลาด: {str(e)}'
#         }, status=500)


# @require_http_methods(["GET"])
# def get_bill(request, bill_id):
#     """ดึงข้อมูลใบแจ้งหนี้"""
#     try:
#         bill = get_object_or_404(CmtArtr, id=bill_id)
#         items = bill.bill_items.all().order_by('row_number')

#         data = {
#             'id': bill.id,
#             'bill_no': bill.bill_no,
#             'date': bill.date.strftime('%Y-%m-%d'),
#             'month': bill.month,
#             'year': bill.year,
#             'prd': bill.prd,
#             'room_no_1': bill.room_no_1,
#             'room_no_2': bill.room_no_2,
#             'member_1': bill.member_1,
#             'member_2': bill.member_2,
#             'duedate': bill.duedate.strftime('%Y-%m-%d'),
#             'remark_1': bill.remark_1,
#             'textstamp': bill.textstamp,
#             'total_before_vat': float(bill.total_before_vat),
#             'vat_amount': float(bill.vat_amount),
#             'total_amount': float(bill.total_amount),
#             'paid_amount': float(bill.paid_amount),
#             'outstanding_amount': float(bill.outstanding_amount),
#             'items': [
#                 {
#                     'row': item.row_number,
#                     'code': item.item_code,
#                     'description': item.description,
#                     'rate': float(item.rate),
#                     'qty': float(item.quantity),
#                     'amount': float(item.amount)
#                 }
#                 for item in items
#             ]
#         }

#         return JsonResponse({
#             'success': True,
#             'data': data
#         })

#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'เกิดข้อผิดพลาด: {str(e)}'
#         }, status=500)


# @require_http_methods(["GET"])
# def search_bills(request):
#     """ค้นหาใบแจ้งหนี้"""
#     try:
#         search_query = request.GET.get("search", "")
#         date_from = request.GET.get("date_from", "")
#         date_to = request.GET.get("date_to", "")
#         page = int(request.GET.get("page", 1))

#         # Query ข้อมูล
#         queryset = CmtArtr.objects.all()

#         # ค้นหา
#         if search_query:
#             queryset = queryset.filter(
#                 Q(bill_no__icontains=search_query)
#                 | Q(member_1__icontains=search_query)
#                 | Q(member_2__icontains=search_query)
#                 | Q(prd__icontains=search_query)
#             )

#         # กรองตามวันที่
#         if date_from:
#             queryset = queryset.filter(date__gte=date_from)
#         if date_to:
#             queryset = queryset.filter(date__lte=date_to)

#         # Pagination
#         paginator = Paginator(queryset, 20)
#         page_obj = paginator.get_page(page)

#         bills = []
#         for bill in page_obj:
#             bills.append({
#                 'id': bill.id,
#                 'bill_no': bill.bill_no,
#                 'date': bill.date.strftime('%Y-%m-%d'),
#                 'month_year': f"{bill.month}/{bill.year}",
#                 'prd': bill.prd,
#                 'member_name': bill.member_2 or bill.member_1,
#                 'duedate': bill.duedate.strftime('%Y-%m-%d'),
#                 'total_amount': float(bill.total_amount),
#                 'paid_amount': float(bill.paid_amount),
#                 'outstanding_amount': float(bill.outstanding_amount)
#             })

#         return JsonResponse({
#             'success': True,
#             'data': {
#                 'bills': bills,
#                 'pagination': {
#                     'current_page': page_obj.number,
#                     'total_pages': page_obj.paginator.num_pages,
#                     'total_records': page_obj.paginator.count,
#                     'start_index': page_obj.start_index(),
#                     'end_index': page_obj.end_index(),
#                     'has_previous': page_obj.has_previous(),
#                     'has_next': page_obj.has_next()
#                 }
#             }
#         })

#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'เกิดข้อผิดพลาด: {str(e)}'
#         }, status=500)


# @require_http_methods(["GET"])
# def generate_bill_no(request):
#     """สร้างเลขที่ใบแจ้งหนี้ใหม่"""
#     try:
#         today = date.today()
#         year = today.year
#         month = today.month

#         # หาเลขที่ล่าสุดในเดือนนี้
#         prefix = f"INV{year}{month:02d}"
#         last_bill = CmtArtr.objects.filter(
#             bill_no__startswith=prefix
#         ).order_by('-bill_no').first()

#         if last_bill:
#             # ดึงเลขลำดับจากเลขที่ล่าสุด
#             try:
#                 last_sequence = int(last_bill.bill_no[-3:])
#                 new_sequence = last_sequence + 1
#             except ValueError:
#                 new_sequence = 1
#         else:
#             new_sequence = 1

#         new_bill_no = f"{prefix}{new_sequence:03d}"

#         return JsonResponse({
#             'success': True,
#             'bill_no': new_bill_no
#         })

#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'เกิดข้อผิดพลาด: {str(e)}'
#         }, status=500)


# @require_http_methods(["GET"])
# def print_bill(request, bill_id):
#     """พิมพ์ใบแจ้งหนี้"""
#     try:
#         bill = get_object_or_404(CmtArtr, id=bill_id)
#         items = bill.bill_items.all().order_by('row_number')

#         context = {
#             'bill': bill,
#             'items': items,
#         }

#         return render(request, 'm34/print_bill.html', context)

#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'เกิดข้อผิดพลาด: {str(e)}'
#         }, status=500)


# # Form-based views (ทางเลือกสำหรับใช้แบบ traditional form)
# def create_bill_form(request):
#     """สร้างใบแจ้งหนี้แบบ form"""
#     if request.method == 'POST':
#         try:
#             with transaction.atomic():
#                 # สร้างใบแจ้งหนี้หลัก
#                 bill = CmtArtr.objects.create(
#                     bill_no=request.POST.get('bill_no'),
#                     date=datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date(),
#                     month=request.POST.get('month'),
#                     year=request.POST.get('year'),
#                     prd=request.POST.get('prd', ''),
#                     room_no_1=request.POST.get('room_no_1', ''),
#                     room_no_2=request.POST.get('room_no_2', ''),
#                     member_1=request.POST.get('member_1'),
#                     member_2=request.POST.get('member_2', ''),
#                     duedate=datetime.strptime(request.POST.get('duedate'), '%Y-%m-%d').date(),
#                     remark_1=request.POST.get('remark_1', ''),
#                     textstamp=request.POST.get('textstamp', ''),
#                     paid_amount=Decimal(request.POST.get('paid_amount', 0) or 0)
#                 )

#                 # สร้างรายการสินค้า
#                 for i in range(1, 16):  # 15 แถว
#                     code = request.POST.get(f'item_code_{i}', '')
#                     description = request.POST.get(f'item_description_{i}', '')
#                     rate = request.POST.get(f'item_rate_{i}', 0)
#                     qty = request.POST.get(f'item_qty_{i}', 0)

#                     if code or description or float(rate or 0) > 0 or float(qty or 0) > 0:
#                         CmtArtrItem.objects.create(
#                             bill=bill,
#                             row_number=i,
#                             item_code=code,
#                             description=description,
#                             rate=Decimal(rate or 0),
#                             quantity=Decimal(qty or 0)
#                         )

#                 # คำนวณยอดรวม
#                 bill.calculate_totals()

#                 messages.success(request, 'บันทึกใบแจ้งหนี้เรียบร้อย')
#                 return render(request, 'm34/form_success.html', {'bill': bill})

#         except Exception as e:
#             messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')

#     # สร้างเลขที่ใบแจ้งหนี้ใหม่
#     today = date.today()
#     prefix = f"INV{today.year}{today.month:02d}"
#     last_bill = CmtArtr.objects.filter(bill_no__startswith=prefix).order_by('-bill_no').first()

#     if last_bill:
#         try:
#             last_sequence = int(last_bill.bill_no[-3:])
#             new_sequence = last_sequence + 1
#         except ValueError:
#             new_sequence = 1
#     else:
#         new_sequence = 1

#     new_bill_no = f"{prefix}{new_sequence:03d}"

#     context = {
#         'new_bill_no': new_bill_no,
#         'today': today.strftime('%Y-%m-%d'),
#         'due_date': (today.replace(day=28) if today.day > 28 else today.replace(day=today.day + 15)).strftime('%Y-%m-%d'),
#         'current_month': f"{today.month:02d}",
#         'buddhist_year': str(today.year + 543)
#     }

#     return render(request, 'm34/create_form.html', context)
from django.shortcuts import render
from expense.models import CmtArtr, CmtArtrItem
from expense.forms import CmtArtrForm
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

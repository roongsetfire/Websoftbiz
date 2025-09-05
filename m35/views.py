from django.shortcuts import render
from m35.forms import CmtRctrForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CmtRctr
from m34.models import CmtArtrItem, CmtArtr
import json
from django.core.serializers.json import DjangoJSONEncoder

@csrf_exempt
def delete_record(request, pk):
    if request.method == "DELETE":
        try:
            record = CmtRctr.objects.get(pk=pk)
            record.delete()
            return JsonResponse({"status": "success", "message": "Record deleted successfully."})
        except CmtRctr.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Record not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


def m35(request):

    # ---------- กรณี GET ข้อมูลรายการบิล (AJAX) ----------
    if request.method == "GET" and request.GET.get("action") == "get_items":
        r_c_no = request.GET.get("r_c_no")
        if not r_c_no:
            return JsonResponse({"status": "error", "message": "ไม่พบ r_c_no"}, status=400)

        items = list(
            CmtArtrItem.objects.filter(textstamp=r_c_no).values(
                "bill_no", "item_code", "m_y_prd", "description", "rate", "quantity", "amount"
            )
        )
        return JsonResponse({"status": "success", "items": items})

    # ---------- POST (save ใบเสร็จ + update textstamp) ----------
    if request.method == "POST":
        form = CmtRctrForm(request.POST)
        record_id = request.POST.get('id')

        if record_id:
            try:
                instance = CmtRctr.objects.get(pk=record_id)
                form = CmtRctrForm(request.POST, instance=instance)
            except CmtRctr.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'ไม่พบข้อมูลเดิม'}, status=404)

        if form.is_valid():
            saved = form.save()
            r_c_no = saved.r_c_no  # ✅ เลขที่ใบเสร็จ

            # ✅ update textstamp ของบิล (ถ้ามีส่งมาจาก frontend)
            bills_json = request.POST.get("bills")
            if bills_json:
                try:
                    bills = json.loads(bills_json)
                    updated_count = 0
                    for bill in bills:
                        bill_no = bill.get("bill_no")
                        item_code = bill.get("item_code")
                        m_y_prd = bill.get("m_y_prd")

                        if bill_no and item_code and m_y_prd:
                            updated = CmtArtrItem.objects.filter(
                                bill_no=bill_no,
                                item_code=item_code,
                                m_y_prd=m_y_prd
                            ).update(textstamp=r_c_no)
                            updated_count += updated

                    return JsonResponse({
                        'status': 'success',
                        'message': 'บันทึกเรียบร้อยแล้ว!',
                        'updated': updated_count
                    })

                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': f'อัปเดต textstamp ผิดพลาด: {str(e)}'}, status=500)

            return JsonResponse({'status': 'success', 'message': 'บันทึกเรียบร้อยแล้ว!'})

        else:
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'message': 'ข้อมูลไม่ถูกต้อง', 'errors': errors}, status=400)

    # ---------- GET ปกติ (render template) ----------
    data = CmtRctr.objects.all().order_by('id')
    data_value = CmtRctr.objects.all().values().order_by('-id')
    data_artr = CmtArtr.objects.all().values().order_by('-id')
    # data_table = CmtArtrItem.objects.all().values().order_by('id')
    data_table = CmtArtrItem.objects.filter(textstamp='unpaid').values().order_by('id')
    data_table_json = list(data_table)
    data_list = list(data_value)
    data_artr1 = list(data_artr)

    context = {
        'row_numbers': range(1, 10),  # 1 ถึง 10
        'unpaid_list': [1, 2, 3, 4, 5, 6, 7, 8],
        'payment_choices': CmtRctr.PAYMENT_CHOICES,
        'type_choices': CmtRctr.TYPE_CHOICES,
        'data': data,
        'data_json': json.dumps(data_list, cls=DjangoJSONEncoder),
        'data_artr': json.dumps(data_artr1, cls=DjangoJSONEncoder),
        'data_table': data_table,
        'data_table_json': json.dumps(data_table_json, cls=DjangoJSONEncoder)
    }

    return render(request, 'm35/index.html', context)

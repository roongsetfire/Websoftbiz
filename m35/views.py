from django.shortcuts import render
from m35.forms import CmtRctrForm
from django.contrib import messages
from django.http import HttpResponse
from .models import CmtRctr
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


def m35(request):

    data = CmtRctr.objects.all().order_by('id')
    data_value = CmtRctr.objects.all().values().order_by('-id')
    data_list = list(data_value)
    if request.method == "POST":
        form = CmtRctrForm(request.POST)
        record_id = request.POST.get('id')

        if record_id:
            try:
                instance = CmtRctr.objects.get(pk=record_id)  # ✅ โหลด record เดิม
                form = CmtRctrForm(request.POST, instance=instance)  # ✅ ใช้ instance เดิม
            except CmtRctr.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'ไม่พบข้อมูลเดิม'}, status=404)
            
        if form.is_valid():
            form.save()
            # messages.success(request, "เพิ่มเรียบร้อยแล้ว!")
            return JsonResponse({'status': 'success', 'message': 'เพิ่มเรียบร้อยแล้ว!'})
        else:
            # print("Form errors:", form.errors)  # ✅ DEBUG ERROR ใน Terminal
            # messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'message': 'ข้อมูลไม่ถูกต้อง', 'errors': errors}, status=400)
    # else:
    #     form = CmtRctrForm()

    # print('form',form)

    context = {
        'row_numbers': range(1, 10),  # 1 ถึง 15
        'unpaid_list' : [1,2,3,4,5,6,7,8],
        'payment_choices' : CmtRctr.PAYMENT_CHOICES,
        'type_choices' : CmtRctr.TYPE_CHOICES,
        'data' : data,
        'data_json' : json.dumps(data_list, cls=DjangoJSONEncoder)
        
    }
    print(list(CmtRctr.objects.values()))
    # print('check',context['data_json'])
    return render(request,'m35/index.html',context)


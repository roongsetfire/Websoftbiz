from django.shortcuts import render
from m35.forms import CmtRctrForm
from django.contrib import messages
from django.http import HttpResponse
from .models import CmtRctr
import json
from django.core.serializers.json import DjangoJSONEncoder

def m35(request):

    data = CmtRctr.objects.all()
    data_value = CmtRctr.objects.all().values()
    data_list = list(data_value)
    if request.method == "POST":
        form = CmtRctrForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "เพิ่มเรียบร้อยแล้ว!")
        else:
            messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    else:
        form = CmtRctrForm()

    context = {
        'row_numbers': range(1, 10),  # 1 ถึง 15
        'unpaid_list' : [1,2,3,4,5,6,7,8],
        'payment_choices' : CmtRctr.PAYMENT_CHOICES,
        'type_choices' : CmtRctr.TYPE_CHOICES,
        'data' : data,
        'data_json' : json.dumps(data_list, cls=DjangoJSONEncoder)
        
    }
    print(list(CmtRctr.objects.values()))
    print('check',context['data_json'])
    return render(request,'m35/index.html',context)


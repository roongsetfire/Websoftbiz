from django.shortcuts import render
from expense.models import CmtArtr, CmtArtrItem
from expense.forms import CmtArtrForm
from django.contrib import messages
from django.http import HttpResponse

def m35(request):
    context = {
        'row_numbers': range(1, 10),  # 1 ถึง 15
        'unpaid_list' : [1,2,3,4,5,6,7,8]
        
    }
    return render(request,'m35/index.html',context)


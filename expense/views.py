from django.shortcuts import render, redirect, get_object_or_404
from .models import CmtArtr
from .forms import CmtArtrForm
from django.contrib import messages


def expense_list(request):
    expenses = CmtArtr.objects.all()
    return render(request, "expense/expense-list.html", {"expenses": expenses})


def expense_create(request):
    if request.method == "POST":
        form = CmtArtrForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกใบเสร็จเรียบร้อยแล้ว!")
            return redirect("expense-list-page")
    else:
        form = CmtArtrForm()
    return render(request, "expense/expense-form.html", {"form": form})


def expense_edit(request, pk):
    expense = get_object_or_404(CmtArtr, pk=pk)
    if request.method == "POST":
        form = CmtArtrForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "แก้ไขใบเสร็จเรียบร้อยแล้ว!")
            return redirect("expense-list-page")
    else:
        form = CmtArtrForm(instance=expense)
    return render(request, "expense/expense-form.html", {"form": form})


def expense_delete(request, pk):
    expense = get_object_or_404(CmtArtr, pk=pk)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "ลบใบเสร็จเรียบร้อยแล้ว!")
        return redirect("expense-list-page")
    return render(request, "expense/expense-confirm-delete.html", {"expense": expense})

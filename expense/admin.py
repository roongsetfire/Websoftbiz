# admin.py
from django.contrib import admin
from .models import CmtArtr, CmtArtrItem


@admin.register(CmtArtr)
class CmtArtrAdmin(admin.ModelAdmin):
    list_display = ["bill_no", "date", "member_1", "prd", "remark_1", "timestamp"]
    list_filter = ["date", "year", "month", "prd", "timestamp"]
    search_fields = ["bill_no", "member_1", "member_2", "prd", "remark_1", "textstamp"]
    list_per_page = 25
    date_hierarchy = "date"
    ordering = ["-timestamp", "-date"]

    fieldsets = (
        ("ข้อมูลใบเสร็จ", {"fields": ("bill_no", "date", "month", "year")}),
        (
            "ข้อมูลห้องและสมาชิก",
            {"fields": ("prd", "room_no_1", "room_no_2", "member_1", "member_2")},
        ),
        ("ข้อมูลการชำระ", {"fields": ("duedate", "remark_1")}),
        (
            "หมายเหตุและเวลา",
            {"fields": ("textstamp", "timestamp"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ["timestamp"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related()


# Customize admin site header
admin.site.site_header = "Softbiz Administration"
admin.site.site_title = "Softbiz Admin"
admin.site.index_title = "จัดการระบบใบเสร็จ"

@admin.register(CmtArtrItem)
class CmtArtrItemAdmin(admin.ModelAdmin):
    list_display = ['room_no','m_y_prd',"bill_no", "row_number", "item_code", "description", "rate", "quantity", "amount"]
from django.contrib import admin
from .models import CmtRctr

# Register your models here.
@admin.register(CmtRctr)
class CmtArtrAdmin(admin.ModelAdmin):
    list_display = ("r_c_no", "date", "room_no_1", "member_1", "timestamp")
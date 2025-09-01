# models.py
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class CmtArtr(models.Model):
    bill_no = models.CharField(max_length=50, unique=True, verbose_name="เลขที่ใบแจ้งหนี้")
    date = models.DateField(verbose_name="วันที่")
    month = models.CharField(max_length=10, verbose_name="ประจำเดือน")
    year = models.CharField(max_length=10, verbose_name="ปี")
    prd = models.CharField(max_length=20, blank=True, null=True, verbose_name="งวด")

    room_no_1 = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="เลขที่ห้อง 1"
    )
    room_no_2 = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="เลขที่ห้อง 2"
    )
    member_1 = models.CharField(max_length=100, verbose_name="รหัส-ชื่อ 1")
    member_2 = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="รหัส-ชื่อ 2"
    )

    duedate = models.DateField(verbose_name="ชำระภายในวันที่")
    remark_1 = models.TextField(blank=True, null=True, verbose_name="หมายเหตุ 1")
    remark_2 = models.CharField(blank=True, null=True, verbose_name="หมายเหตุ 2")

    # Summary fields
    total_before_vat = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="มูลค่าก่อนภาษี"
    )
    vat_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="ภาษีมูลค่าเพิ่ม"
    )
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="รวมเงินทั้งสิ้น"
    )
    paid_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="ยอดชำระแล้ว"
    )
    outstanding_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="ยอดค้างชำระ"
    )

    timestamp = models.DateTimeField(default=timezone.now, verbose_name="เวลาบันทึก")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="เวลาอัพเดท")

    class Meta:
        db_table = "CMT_ARTR"
        verbose_name = "ข้อมูลใบเสร็จ"
        verbose_name_plural = "ข้อมูลใบเสร็จทั้งหมด"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.bill_no} - {self.member_1}"

    def calculate_totals(self):
        """คำนวณยอดรวมจากรายการสินค้า"""
        items = self.bill_items.all()
        total = sum(item.amount for item in items)

        vat_rate = Decimal("0.07")  # 7% VAT
        self.total_before_vat = total / (1 + vat_rate)
        self.vat_amount = total - self.total_before_vat
        self.total_amount = total
        self.outstanding_amount = self.total_amount - self.paid_amount

        self.save(
            update_fields=[
                "total_before_vat",
                "vat_amount",
                "total_amount",
                "outstanding_amount",
            ]
        )


class CmtArtrItem(models.Model):
    room_no = models.CharField(max_length=10, default="-", verbose_name="หมายเลขห้อง")
    m_y_prd = models.CharField(max_length=20, default="-", verbose_name="เดือน/ปี/งวด")
    bill_no = models.CharField(max_length=20, default="-", verbose_name="เลขที่บิลล์")
    item_code = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="รหัส"
    )
    description = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="รายงาน"
    )
    rate = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="อัตรา"
    )
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="จำนวน"
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="เป็นเงิน"
    )

    created_at = models.DateTimeField(default=timezone.now, verbose_name="เวลาสร้าง")

    textstamp = models.CharField(
        max_length=50, default="unpaid", verbose_name="ตรวจสอบการชำระบิล"
    )

    class Meta:
        db_table = "CMT_ARTR_ITEM"
        verbose_name = "รายการใบแจ้งหนี้"
        verbose_name_plural = "รายการใบแจ้งหนี้ทั้งหมด"
        ordering = ["created_at"]  # เปลี่ยนจาก row_number เป็น created_at

    def save(self, *args, **kwargs):
        # คำนวณยอดเงินอัตโนมัติ
        self.amount = self.rate * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bill_no} - {self.item_code}"  # เปลี่ยนจาก row_number

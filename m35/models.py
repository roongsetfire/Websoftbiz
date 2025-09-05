# Create your models here.
# models.py
from django.db import models
# from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class CmtRctr(models.Model):
    TYPE_CHOICES = [
        ("ชำระตามบิล", "ชำระตามบิล"),
        ("จ่ายล่วงหน้า", "จ่ายล่วงหน้า"),
        ("รายรับอื่นๆ", "รายรับอื่นๆ"),
    ]

    PAYMENT_CHOICES = [
        ("เงินสด", "เงินสด"),
        ("เช็ค", "เช็ค"),
        ("เงินโอน", "เงินโอน"),
        ("อื่นๆ","อื่นๆ")
    ]

    r_c_no = models.CharField(max_length=50, unique=True, verbose_name="เลขที่ใบเสร็จ")
    date = models.DateField(verbose_name="วันที่")
    payin = models.DateField(blank=True, null=True,verbose_name="ฝาก")

    room_no_1 = models.CharField(
        max_length=20, verbose_name="เลขที่ห้อง 1"
    )
    room_no_2 = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="เลขที่ห้อง 2"
    )

    member_1 = models.CharField(max_length=100, verbose_name="รหัส-ชื่อ 1")
    member_2 = models.CharField(max_length=100, blank=True, null=True, verbose_name="รหัส-ชื่อ 2")

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="ประเภท",
        blank=True, null=True  # หากไม่ต้องเลือกก็ใส่ True ทั้งคู่
    )

    payment_method = models.CharField(
    max_length=20,
    choices=PAYMENT_CHOICES,
    verbose_name="ชำระโดย",
    blank=True,
    null=True
    )

    bank_1 = models.CharField(blank=True, null=True,max_length=100, verbose_name="ธนาคาร 1")
    bank_2 = models.CharField(max_length=100, blank=True, null=True, verbose_name="ธนาคาร 2")

    bank_no = models.CharField(blank=True, null=True,max_length=20, verbose_name="เลขที่")
    bank_date = models.DateField(blank=True, null=True,verbose_name="วันที่(ธนาคาร)")

    vat = models.BooleanField(blank=True, null=True,default=False, verbose_name="ภาษีหักณที่จ่าย")

    deduct_from_prepaid = models.BooleanField(blank=True, null=True,default=False, verbose_name="ลดหนี้จากการชำระล่วงหน้า")
    withdraw_from_bankaccount = models.BooleanField(blank=True, null=True,default=False, verbose_name="ตัดบัญชีเงินฝากส่วนตัว")
    withdraw = models.CharField(max_length=100, blank=True, null=True, verbose_name="ตัดบัญชีเงินฝากส่วนตัว(กรอก)")

    total = models.CharField(max_length=100, blank=True, null=True, verbose_name="ยอดชำระสุทธิ")

    tax_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="เลขที่หนังสือรับรองการหักภาษี")
    tax_date = models.DateField(blank=True, null=True,verbose_name="ลงวันที่")

    no_ref = models.CharField(max_length=20, blank=True, null=True, verbose_name="เลขที่อ้างอิง")
   

    remark_1 = models.TextField(blank=True, null=True, verbose_name="หมายเหตุ 1")
    remark_2 = models.TextField(blank=True, null=True, verbose_name="หมายเหตุ 2")

    textstamp = models.CharField(blank=True, null=True, verbose_name="textstamp")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="เวลาอัพเดท")

    class Meta:
        db_table = "CMT_RCTR"
        verbose_name = "ใบเสร็จรับเงิน"
        verbose_name_plural = "ใบเสร็จรับเงินทั้งหมด"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.r_c_no} - {self.member_1}"

from django.db import models
from authenticate.models import User
import django_jalali.db.models as jmodels
from django.utils import timezone
import jdatetime
from django.utils.html import format_html
import pytz



class level_1(models.Model):
    class type(models.IntegerChoices):
        TYPE_1 = 1, 'چرخ خیاطی'
        TYPE_2 = 2, 'اتو پرس'
        TYPE_3 = 3, 'اتو مخزن دار'
    types=models.IntegerField(choices=type.choices,default=0,verbose_name='نوع دستگاه')
    model=models.CharField(max_length=255,verbose_name='مدل')
    pic_machine = models.ImageField(upload_to='data/machine/',verbose_name='تصویر دستگاه',null=True,blank=True)
    serial=models.CharField(max_length=255,verbose_name='سریال')
    pic_serial = models.ImageField(upload_to='data/serial/',verbose_name='تصویر سریال',null=True,blank=True)
    brand_name= models.CharField(max_length=50,verbose_name='نام برند',blank=True,null=True)
    price= models.IntegerField(verbose_name='قیمت',blank=True,null=True)
    date= jmodels.jDateField(null=True,blank=True,verbose_name='تاریخ شروع گارانتی')
    end_date= jmodels.jDateField(null=True,blank=True,verbose_name='تاریخ پایان گارانتی')
    is_approved = models.BooleanField(default=False,verbose_name='تایید')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='level1_submissions',null=True,blank=True)
    def PicMachine(self):
        if self.pic_machine:
            return format_html(f'<img src="{format(self.pic_machine.url)}" width="100" height="100" />')
        return 'دستگاه عکسی ندارد'

    PicMachine.short_description = "پیش نمایش"
    PicMachine.allow_tags = True
    def PicSerial(self):
        if self.pic_serial:
            return format_html(f'<img src="{format(self.pic_serial.url)}" width="100" height="100" />')
        return 'سریال عکسی ندارد'

    PicSerial.short_description = "پیش نمایش"
    PicSerial.allow_tags = True
    def save(self, *args, **kwargs):
        now = timezone.now()
        tehran_timezone = pytz.timezone('Asia/Tehran')
        now = now.astimezone(tehran_timezone)
        now_jalali = jdatetime.datetime.fromgregorian(datetime=now)
        if not self.date:
            self.date=now_jalali
        if not self.end_date:
            end_date_jalali = self.date + jdatetime.timedelta(days=730)
            self.end_date = end_date_jalali
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'گارانتی'
        verbose_name_plural = 'گارانتی ها'

    def __str__(self):
        return f'id: {self.id}'
class Level_2(models.Model):
    payment_receipt = models.ImageField(upload_to='data/receipts/',verbose_name='تصویر پرداختی')
    serial_payment = models.CharField(max_length=255,verbose_name='سریال پرداخت')
    is_approved = models.BooleanField(default=False,verbose_name='تایید')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='level2_submissions',verbose_name='کاربر')
    level1 = models.OneToOneField(level_1, on_delete=models.CASCADE,verbose_name='گارانتی')
    code = models.CharField(max_length=8,null=True, blank=True,verbose_name='کد')


    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداختی ها'

    def __str__(self):
        return f"id: {self.id}"

    def image_tag(self):
        if self.payment_receipt:
            return format_html(f'<img src="{format(self.payment_receipt.url)}" width="100" height="100" />')
        return 'کالا عکسی ندارد'

    image_tag.short_description = "پیش نمایش"
    image_tag.allow_tags = True
class Level_3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='level3_submissions', verbose_name='کاربر')
    level1 = models.OneToOneField(level_1, on_delete=models.CASCADE,verbose_name='گارانتی')
    level2 = models.OneToOneField(Level_2, on_delete=models.CASCADE,verbose_name='پرداختی ها')
    submission_date = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'تایید نهایی'
        verbose_name_plural = 'تایید نهایی'
    def save(self, *args, **kwargs):
        now = timezone.now()
        tehran_timezone = pytz.timezone('Asia/Tehran')
        now = now.astimezone(tehran_timezone)
        now_jalali = jdatetime.datetime.fromgregorian(datetime=now)
        if not self.submission_date:
            self.submission_date = now_jalali
        super().save(*args, **kwargs)



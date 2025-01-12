from django.contrib import admin
from .models import level_1,Level_2 ,Level_3
import django_jalali.db.models as jmodels
from django_jalali.admin.widgets import AdminjDateWidget

@admin.register(level_1)
class level_1_admin(admin.ModelAdmin):
    list_display = ('types','model', 'serial','price','brand_name','date','end_date', 'is_approved','id')
    actions = ['approve']
    list_editable = ['is_approved']
    list_filter = ['types','model','is_approved']
    readonly_fields = ['id','date','end_date','types','model','brand_name','serial','price','user','PicMachine','PicSerial']
    list_per_page = 15
    fieldsets = (
        ('مشخصات کالا', {
            'fields': ('id', 'types', 'model','pic_machine','PicMachine','serial','pic_serial','PicSerial','brand_name')
        }),
        ('قیمت محصول',
            {
                'fields':('price',)
        }),
        ('تاریخ',
         {
             'fields': ('date','end_date')
        }),
        ('تایید',
         {
             'fields': ('user','is_approved')
         }),
    )
    def approve(self, request, queryset):
        queryset.update(is_approved=True)

    approve.short_description = "تایید موارد انتخاب شده"

    formfield_overrides = {
        jmodels.jDateField: {'widget': AdminjDateWidget},
    }

@admin.register(Level_2)
class Level2Admin(admin.ModelAdmin):
    list_display = ('user','serial_payment','code','image_tag','level1', 'is_approved','id')
    actions = ['approve']
    list_editable = ['is_approved']
    readonly_fields = ['image_tag','user','serial_payment','id','level1','code']
    fieldsets = (
        ('تصویر فیش',
         {
             'fields': ('id','payment_receipt', 'image_tag')
         }),
        ('سریال',
         {
             'fields': ('serial_payment',)
         }),
        ('اطلاعات اضافه',
         {
             'fields': ('user','level1','code')
         }),
        ('تایید',
         {
             'fields': ('is_approved',)
         }),
    )
    def approve(self, request, queryset):
        queryset.update(is_approved=True)
    approve.short_description = "تایید فیش‌های انتخاب شده"


@admin.register(Level_3)
class Level3Admin(admin.ModelAdmin):
    list_display = ['user','level1','level2','submission_date','id']
    readonly_fields = ['user','level1','level2','submission_date','id']
    fieldsets = (
        ('اطلاعات',
         {
             'fields': ('id','user','level1','level2','submission_date')
         }),
    )

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from .models import User,OTP,CodeGenerator,GeneratedCode,CodeGeneratorForm
from warranty.models import level_1,Level_2,Level_3
from import_export.admin import ExportActionModelAdmin



class Level1Inline(admin.TabularInline):
    model = level_1
    extra = 0

    def id_field(self, obj):
        return obj.id
    id_field.short_description = 'ID'

    readonly_fields = ['id_field','types','model','serial','brand_name','price','date', 'end_date']

    def has_add_permission(self, request, obj=None):
        return False

class Level2Inline(admin.TabularInline):
    model = Level_2
    extra = 0
    def id_field(self, obj):
        return obj.id
    id_field.short_description = 'ID'

    readonly_fields = ['id_field','payment_receipt','code','image_tag','serial_payment','level1']

    def has_add_permission(self, request, obj=None):
        return False

class Level3Inline(admin.TabularInline):
    model = Level_3
    extra = 0
    def id_field(self, obj):
        return obj.id
    id_field.short_description = 'ID'

    readonly_fields = ['id_field','level1','level2','submission_date']

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    change_password_form = AdminPasswordChangeForm
    inlines = [Level1Inline, Level2Inline,Level3Inline]
    list_display = ('phone_number', 'full_name', 'national_id','code', 'is_active')
    search_fields = ('phone_number', 'full_name', 'national_id','code')
    ordering = ('phone_number',)
    fieldsets = (
        ('کاربر', {'fields': ('phone_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'national_id','code', 'address','postal_code')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('مهم', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'national_id', 'password1', 'password2'),
        }),
    )
@admin.register(OTP)
class otp_admin(admin.ModelAdmin):
    list_display = ['phone_number','otp','created_at','expires_at']

@admin.register(GeneratedCode)
class GeneratedCodeAdmin(ExportActionModelAdmin,admin.ModelAdmin):
    list_display = ['code','is_active','assigned', 'created_at']
    list_filter = ['assigned','is_active']
    search_fields = ['code']

@admin.register(CodeGenerator)
class CodeGeneratorAdmin(admin.ModelAdmin):
    list_display = ['number_of_codes']
    form = CodeGeneratorForm
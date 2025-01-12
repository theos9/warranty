from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import random
from django import forms

class GeneratedCode(models.Model):
    code = models.CharField(max_length=8, unique=True,verbose_name='کد')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ تولید')
    assigned = models.BooleanField(default=False,verbose_name='اختصاص داده شده')
    is_active= models.BooleanField(default=False,verbose_name='فعال/غیر فعال')
    class Meta:
        verbose_name = 'کد جدید'
        verbose_name_plural ='کد های تولید شده'
    def __str__(self):
        return self.code

class CodeGenerator(models.Model):
    number_of_codes = models.IntegerField(default=1,verbose_name='تعداد کد ها')
    class Meta:
        verbose_name = 'تعداد'
        verbose_name_plural ='تولید کد'
    def generate_codes(self):
        codes = []
        for _ in range(self.number_of_codes):
            while True:
                code = str(random.randint(10000, 99999999))
                if not GeneratedCode.objects.filter(code=code).exists():
                    GeneratedCode.objects.create(code=code)
                    codes.append(code)
                    break
        return codes

class CodeGeneratorForm(forms.ModelForm):
    class Meta:
        model = CodeGenerator
        fields = ['number_of_codes']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.generate_codes()
        instance.save()
        return instance

class UserManager(BaseUserManager):
    def create_user(self, phone_number, national_id, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('شماره تماس باید وارد شود')
        if not national_id:
            raise ValueError('کد ملی باید وارد شود')

        user = self.model(phone_number=phone_number, national_id=national_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, national_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, national_id, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True,verbose_name='شماره تماس')
    full_name = models.CharField(max_length=60,verbose_name='نام و نام خانوادگی',blank=True,null=True)
    national_id = models.CharField(max_length=10, unique=True,verbose_name='کد ملی')
    address= models.CharField(max_length=255,verbose_name='ادرس',blank=True,null=True)
    postal_code = models.CharField(max_length=10,verbose_name='کد پستی',blank=True,null=True)
    is_active = models.BooleanField(default=1,verbose_name='فعال/غیر فعال')
    is_staff = models.BooleanField(default=False,verbose_name='کارمند')
    is_superuser = models.BooleanField(default=False)
    code = models.OneToOneField(GeneratedCode, null=True, blank=True, on_delete=models.SET_NULL,verbose_name='کد')

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name', 'national_id']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural ='کاربرها'
    def __str__(self):
        return f'user: {self.full_name}'


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )
class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    class Meta:
        verbose_name = 'رمز یکبار مصرف'
        verbose_name_plural ='رمز یکبار مصرف'
    def is_valid(self):
        if timezone.now() > self.expires_at:
            if OTP.objects.filter(id=self.id).exists():
                self.delete()
            return False
            super().is_valid(*args, **kwargs)
        return True

    def generate_expiration(self):
        self.expires_at = timezone.now() + timezone.timedelta(minutes=15)




from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, OTP, GeneratedCode
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
import http
import json
from django.utils import timezone
from .serializer import UserSerializer


class RegisterView(APIView):
    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def generate_unique_code(self):
        while True:
            new_code = str(random.randint(10000, 99999999))
            if not GeneratedCode.objects.filter(code=new_code).exists():
                return new_code

    def assign_code_to_user(self, user):
        code = GeneratedCode.objects.filter(assigned=False).first()

        if code:
            code.assigned = True
            code.save()
        else:
            new_code = self.generate_unique_code()
            code = GeneratedCode.objects.create(code=new_code, assigned=True)

        user.code = code
        user.save()

    def get(self, request, *args, **kwargs):
        phone_number = request.query_params.get('phone_number')

        if not phone_number:
            return Response({'error': 'وارد کردن شماره تماس الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'این شماره تماس قبلاً ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = self.generate_otp()

        expires_at = timezone.now() + timezone.timedelta(minutes=15)
        otp_entry, created = OTP.objects.update_or_create(
            phone_number=phone_number,
            defaults={'otp': otp_code, 'expires_at': expires_at}
        )

        conn = http.client.HTTPSConnection("api.sms.ir")
        payload = json.dumps({
            "mobile": f"{phone_number}",
            "templateId": 123456,
            "parameters": [
                {
                    "name": "CODE",
                    "value": f"{otp_code}"
                }
            ]
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/plain',
            'X-API-KEY': 'hWiijhqcGxXsSGgXNV1IrvnD0'
        }
        conn.request("POST", "/v1/send/verify", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data.decode("utf-8")
        return Response({'message': 'OTP با موفقیت ارسال شد.'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        full_name = request.data.get('full_name')
        national_id = request.data.get('national_id')
        address = request.data.get('address')
        postal_code = request.data.get('postal_code')
        if not all([phone_number, otp, full_name, national_id, address, postal_code]):
            return Response({'error': 'تمامی فیلدهای ضروری وارد نشده‌اند.'}, status=status.HTTP_400_BAD_REQUEST)
        if OTP.objects.filter(phone_number=phone_number).exists():
            otp_entry = OTP.objects.get(phone_number=phone_number)
            if not otp_entry.is_valid() or otp_entry.otp != otp:
                return Response({'error': 'OTP نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)
            elif otp_entry.is_valid() or otp_entry.otp == otp:
                user = User.objects.create(phone_number=phone_number,
                                           full_name=full_name,
                                           national_id=national_id,
                                           address=address,
                                           postal_code=postal_code
                                           )

                user.save()
                otp_entry.delete()
                self.assign_code_to_user(user)

                conn = http.client.HTTPSConnection("api.sms.ir")
                payload = json.dumps({
                    "mobile": f"{phone_number}",
                    "templateId": 123456,
                    "parameters": [
                        {
                            "name": "USER",
                            "value": f"{full_name}"
                        }
                    ]
                })

                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'text/plain',
                    'X-API-KEY': 'hWiijhqcGxXsSGgXNV1IrvnD0y'
                }
                conn.request("POST", "/v1/send/verify", payload, headers)
                res = conn.getresponse()
                data = res.read()
                data.decode("utf-8")

                refresh = RefreshToken.for_user(user)
                return Response({
                    "full_name": str(user.full_name),
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "message": "کاربر با موفقیت ثبت شد"
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'OTP برای این شماره تماس پیدا نشد.'}, status=status.HTTP_400_BAD_REQUEST)


class OTPLoginView(APIView):
    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if not phone_number or not otp:
            return Response({'error': 'شماره تماس و رمز یکبار مصرف باید وارد شوند'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"error": "کاربری با این شماره تماس وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        otp_instance = OTP.objects.filter(phone_number=phone_number).first()
        if otp_instance is None or not otp_instance.is_valid() or otp_instance.otp != otp:
            return Response({"error": "رمز یکبار مصرف نادرست یا منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        otp_instance.delete()

        return Response({
            "full_name": str(user.full_name),
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": "ورود موفقیت‌آمیز بود"
        }, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response({"error": "شماره تماس باید وارد شود."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"error": "کاربری با این شماره تماس وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        new_otp = self.generate_otp()
        OTP.objects.update_or_create(
            phone_number=phone_number,
            defaults={'otp': new_otp, 'expires_at': timezone.now() +
                      timezone.timedelta(minutes=15)}
        )

        conn = http.client.HTTPSConnection("api.sms.ir")
        payload = json.dumps({
            "mobile": f"{phone_number}",
            "templateId": 123456,
            "parameters": [
                {
                    "name": "CODE",
                    "value": f"{new_otp}"
                }
            ]
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/plain',
            'X-API-KEY': 'hWiijhqcGxXsSGgXNV1IrvnD0y'
        }
        conn.request("POST", "/v1/send/verify", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data.decode("utf-8")

        return Response({"message": "OTP جدید ارسال شد."}, status=status.HTTP_200_OK)


class UserDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

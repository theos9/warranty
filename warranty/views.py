from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import level_1, Level_2
from rest_framework.views import APIView
from .serializers import Level2_Serializer ,Level1_Serializer,Level2Serializer
from rest_framework import generics
import json
import http

class Level2SubmissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        level1_id = request.data.get('level1_id')


        if not level1_id:
            return Response({"error": "شناسه‌ی مرحله اول ارسال نشده است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            level1 = level_1.objects.get(id=level1_id, user=user, is_approved=True)
        except level_1.DoesNotExist:
            return Response({"error": "مرحله اول تایید شده‌ای برای این کاربر پیدا نشد."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['user'] = user.id
        data['level1'] = level1.id
        serializer = Level2Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            conn = http.client.HTTPSConnection("api.sms.ir")
            payload = json.dumps({
                "mobile": f"{self.request.user.phone_number}",
                "templateId": 123456,
                "parameters": [
                    {
                        "name": "USER",
                        "value": f"{self.request.user.full_name}"
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
            return Response({"message": "فیش واریز با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Level1ListCreateView(generics.ListCreateAPIView):
    serializer_class = Level1_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return level_1.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        conn = http.client.HTTPSConnection("api.sms.ir")
        payload = json.dumps({
            "mobile": f"{self.request.user.phone_number}",
            "templateId": 123456,
            "parameters": [
                {
                    "name": "USER",
                    "value": f"{self.request.user.full_name}"
                },
                {
                    "name": "CODE",
                    "value": f"{self.request.user.code}"
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

class Level1DetailView(generics.RetrieveAPIView):
    serializer_class = Level1_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return level_1.objects.filter(user=self.request.user)


class Level2ListCreateView(generics.ListAPIView):
    serializer_class = Level2_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Level_2.objects.filter(user=self.request.user)


class Level2DetailView(generics.RetrieveAPIView):
    serializer_class = Level2_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Level_2.objects.filter(user=self.request.user)



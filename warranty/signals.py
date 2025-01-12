from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Level_2, Level_3,level_1
from authenticate.models import GeneratedCode
import json
import http


@receiver(post_save, sender=Level_2)
def create_level3_after_level2_approval(sender, instance, created, **kwargs):
    if not created and instance.is_approved:
        level1 = instance.level1
        if level1.is_approved:
            Level_3.objects.get_or_create(
                user=instance.user,
                level1=level1,
                level2=instance
            )
            user_phone = instance.user.phone_number
            code= instance.user.code
            base_code=GeneratedCode.objects.get(code=code)
            base_code.is_active=True
            base_code.save()

            conn = http.client.HTTPSConnection("api.sms.ir")
            payload = json.dumps({
                "mobile": user_phone,
                "templateId": 716172,
                "parameters": [
                    {
                        "name": "USER",
                        "value": instance.user.full_name
                    },
                    {
                        "name": "CODE",
                        "value": f"{instance.user.code}"
                    },
                    {
                        "name": "PRODUCT",
                        "value": level1.brand_name.format()
                    },
                    {
                        "name": "START_DATE",
                        "value": level1.date.isoformat()
                    },
                    {
                        "name": "END_DATE",
                        "value": level1.end_date.isoformat()
                    }
                ]
            })

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'text/plain',
                'X-API-KEY': 'hWiijhqcGxXsSGgXNV1IrvnD0yjD9vGVeH9XwM83g8S4s9gz2Q9yOFyy0gJMPL5i'
            }

            conn.request("POST", "/v1/send/verify", payload, headers)
            res = conn.getresponse()
            data = res.read()
            data.decode("utf-8")
@receiver(post_save, sender=level_1)
def send_sms_on_approval(sender, instance, **kwargs):
    if instance.is_approved:

        user_phone = instance.user.phone_number
        conn = http.client.HTTPSConnection("api.sms.ir")
        payload = json.dumps({
            "mobile": user_phone,
            "templateId": 417200,
            "parameters": [
                {
                    "name": "USER",
                    "value": instance.user.full_name
                },
                {
                    "name": "PRODUCT",
                    "value": instance.brand_name
                }
            ]
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/plain',
            'X-API-KEY': 'hWiijhqcGxXsSGgXNV1IrvnD0yjD9vGVeH9XwM83g8S4s9gz2Q9yOFyy0gJMPL5i'
        }

        conn.request("POST", "/v1/send/verify", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data.decode("utf-8")

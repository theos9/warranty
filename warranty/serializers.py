from rest_framework import serializers
from .models import Level_2 ,level_1

class Level1_Serializer(serializers.ModelSerializer):
    class Meta:
        model = level_1
        fields = ['id','types', 'model','pic_machine', 'serial','pic_serial','brand_name', 'price', 'date', 'end_date', 'is_approved', 'user']

class Level2_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Level_2
        fields = ['payment_receipt', 'serial_payment','code', 'is_approved', 'user', 'level1']
class Level2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Level_2
        fields = ['payment_receipt', 'serial_payment','code', 'user', 'level1']

        def create(self, validated_data):
            return Level_2.objects.create(**validated_data)



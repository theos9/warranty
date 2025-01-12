from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source='code.code', read_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'full_name',
                  'national_id', 'address', 'postal_code', 'code']

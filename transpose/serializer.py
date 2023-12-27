from rest_framework import serializers
from transpose.models import CheckPidExistModel

class CheckPidExistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckPidExistModel
        fields = ("user_pid",)
from rest_framework import serializers
from runconvert.models import RunConvertModel

class RunConvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunConvertModel
        fields = ("input_music", "output_midi")
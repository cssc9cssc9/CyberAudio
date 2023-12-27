from rest_framework import serializers
from umx.models import UMX, Info

class UMXSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UMX
        
        fields = ("file_path", "model_dir", "output_dir", "do_separate_bass", "do_separate_drums", "do_separate_vocals", "do_separate_other")
    
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        
        fields = ("queue_addr",)
    
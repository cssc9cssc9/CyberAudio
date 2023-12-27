from rest_framework import serializers
from event_handler.models import EventHandlerModel

class EventHandlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventHandlerModel
        fields = ('event_name', 'pid', 'queue_addr', 'progress', 'status', 'update_time')
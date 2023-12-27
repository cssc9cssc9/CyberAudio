
from event_handler.models import EventHandlerModel
from event_handler.serializer import EventHandlerSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

import traceback
import json
# Create your views here.


class EventHandlerViewSet(viewsets.ModelViewSet):
    queryset = EventHandlerModel.objects.all()
    serializer_class = EventHandlerSerializer

    def create(self, request):
        if any([param not in request.data for param in ['event_name', 'pid', 'queue_addr', 'progress', 'status']]):
            return Response({"Request body need to contain ('event_name', 'pid', 'queue_addr', 'progress', 'status')"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    def partial_update(self ,request):
        if any([param not in request.data for param in ['event_name', 'queue_addr']]):
            return Response({"Request body need to contain ('event_name', 'queue_addr')"}, status=status.HTTP_400_BAD_REQUEST)
        if all([param not in request.data for param in ['status', 'progress']]):
            return Response({"Nothing need to be update. One of ('status', 'queue_addr', 'progress') need to be included"}, status=status.HTTP_204_NO_CONTENT)
        with connection.cursor() as cursor:
            sql = f"""
            UPDATE event_handler SET
            """
            for update_param in ['status', 'progress']:
                if update_param in request.data:
                    sql += f" {update_param}='{request.data[update_param]}',"
            sql = sql[:-1]
            sql += f""" WHERE event_name='{request.data["event_name"]}' AND queue_addr='{request.data["queue_addr"]}' """
            cursor.execute(sql)
            response = {"message": "Update successfully."}
            return Response(response, status=status.HTTP_200_OK)

    def get_progress(self, request):
        if any([param not in request.data for param in ['event_name', 'queue_addr']]):
            return Response({"Request body need to contain ('event_name', 'queue_addr')"}, status=status.HTTP_400_BAD_REQUEST)
        sql = f"""SELECT id, progress FROM event_handler WHERE event_name="{request.data['event_name']}" AND queue_addr="{request.data['queue_addr']}" ORDER BY update_time DESC LIMIT 1 """
        qs = EventHandlerModel.objects.raw(sql)
        qs_json = qs[0].__dict__
        response = {'progress':qs_json['progress']}
        return Response(response, status=status.HTTP_200_OK)
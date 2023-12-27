from multiprocessing import Process, Queue
from rest_framework import viewsets, status
from rest_framework.response import Response

from runconvert.models import RunConvertModel
from runconvert.serializer import RunConvertSerializer
from runconvert.interface.music_transcription import music_transcription
from runconvert.apps import RunconvertConfig
import requests
import os
import uuid
# Create your views here.
PROGRESS_QUEUE = Queue()
CONFIG_NAME = RunconvertConfig.name
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
class RunConvertViewSet(viewsets.ModelViewSet):
    queryset = RunConvertModel.objects.all()
    serializer_class = RunConvertSerializer

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        rc_uuid = uuid.uuid1()
        process = Process(target=music_transcription, args=(os.path.join(BASE_DIR, serializer.data["input_music"]),
                                           os.path.join(BASE_DIR, serializer.data["output_midi"]),
                                           rc_uuid, CONFIG_NAME, ))
        process.start()
        requests.post("http://127.0.0.1:8000/_api/model/event_handler/create", data = {"queue_addr": rc_uuid, "pid": process.pid, 'event_name':CONFIG_NAME, 'status': "CREATED", 'progress':0})
        response = {"event_name": CONFIG_NAME, "queue_addr": rc_uuid, "pid": process.pid}
        return Response(response, status=status.HTTP_201_CREATED)                     
    

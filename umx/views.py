import ctypes
from multiprocessing import Process, Queue
from umx.serializers import UMXSerializer, InfoSerializer 
from umx.models import UMX, Info
from rest_framework import viewsets, status
from rest_framework.response import Response
from umx.inference.umx_django import separate, get_latest_progress
from umx.apps import UmxConfig

import requests
import os
import uuid
import json

CONFIG_NAME = UmxConfig.name
PROGRESS_QUEUE = Queue()
#print(id(PROGRESS_QUEUE))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Create your views here.
class UMXViewSet(viewsets.ModelViewSet):
    queryset = UMX.objects.all()
    serializer_class = UMXSerializer
    
    # override post    
    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        umx_uuid = str(uuid.uuid1())
        process = Process(target=separate, args=(os.path.join(BASE_DIR, serializer.data["file_path"]),
                                           os.path.join(BASE_DIR, serializer.data["model_dir"]),
                                           os.path.join(BASE_DIR, serializer.data["output_dir"]), 
                                           serializer.data["do_separate_bass"],
                                           serializer.data["do_separate_drums"],
                                           serializer.data["do_separate_vocals"],
                                           serializer.data["do_separate_other"],
                                           PROGRESS_QUEUE, 
                                           umx_uuid,))
        process.start()
        file_dir = os.path.dirname(serializer.data["file_path"])
        conf_dir = os.path.join(file_dir, "conf")
        if not os.path.exists(conf_dir):
            os.makedirs(conf_dir)
        print(f"{os.path.join(conf_dir, 'header.json')} created" )
        with open(os.path.join(conf_dir, "header.json"), 'w') as fp:
            json.dump(request.data, fp)
        req_data = {"queue_addr": umx_uuid, "pid": process.pid, 'event_name':CONFIG_NAME, 'status': "CREATED", 'progress':0}
        print(req_data)
        requests.post("http://127.0.0.1:8000/_api/model/event_handler/create", data = req_data)
        response = {"event_name": CONFIG_NAME, "queue_addr": umx_uuid, "pid": process.pid}
        return Response(response, status=status.HTTP_201_CREATED)

class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    
    # override post    
    def list(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        progress_queue = ctypes.cast(serializer.data["queue_addr"], ctypes.py_object).value
        progress = get_latest_progress(progress_queue)
        response = {"progress": progress}
        
        return Response(response, status=status.HTTP_201_CREATED)
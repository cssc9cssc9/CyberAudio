from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings


from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response

from transpose.serializer import CheckPidExistSerializer
from transpose.models import CheckPidExistModel

import requests
import json
import time
import os
import psutil
# Create your views here.
@api_view(['POST'])
def upload_audio(request):
    if request.method=="POST":
        upload_file = request.FILES["audio-file"]
        fss = FileSystemStorage()
        # os.makedirs(os.path.join(upload_file.name.rsplit(".", 1)[0]))
        filepath = os.path.join('data', upload_file.name.rsplit(".", 1)[0].replace(" ","_"), upload_file.name.replace(" ","_"))
        if os.path.exists(os.path.join('media', filepath)):
            os.remove(os.path.join('media', filepath))
        file = fss.save(filepath, upload_file)
        response = {"file_name": os.path.join('media', 'data', upload_file.name.rsplit(".", 1)[0].replace(" ","_"), upload_file.name.replace(" ","_"))}
        return Response(response, status=status.HTTP_201_CREATED)


class CheckPidExistViewSet(viewsets.ModelViewSet):
    queryset = CheckPidExistModel.objects.all()
    serializer_class = CheckPidExistSerializer
    http_method_names = ['post']

    def update(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        pid = int(serializer.data['user_pid'])
        response = {"working": int(psutil.pid_exists(pid))}
        return Response(response, status=status.HTTP_200_OK)



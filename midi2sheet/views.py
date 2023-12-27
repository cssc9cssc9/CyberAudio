from django.shortcuts import render

# Create your views here.
from midi2sheet.models import Merge, Sheet, MidiToSheet
from midi2sheet.serializers import MergeSerializer, SheetSerializer, MidiToSheetSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response

from multiprocessing import Process
from midi2sheet.tool.merge import merge_function
from midi2sheet.tool.mi2sh import sheet_function
from midi2sheet.tool.midi_to_sheet import convert_sheet
from midi2sheet.apps import MidiToSheetConfig

import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_NAME = MidiToSheetConfig.name
class MidiToSheetViewSet(viewsets.ModelViewSet):
    queryset = MidiToSheet.objects.all()
    serializer_class = MidiToSheetSerializer 
    def create(self, request):
        with open(os.path.join(BASE_DIR, "midi2sheet", "conf", "midi2sheet_config.json"), 'r') as fp:
            config = json.load(fp)
        tool_dir=  config["tool_dir"]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        process = Process(target=convert_sheet, args=(os.path.join(BASE_DIR, serializer.data["base_dir"]), tool_dir))
        process.start()
        response = {"event_name":CONFIG_NAME, "pid": process.pid}
        return Response(response, status=status.HTTP_201_CREATED)


# Create your views here.
class MergeViewSet(viewsets.ModelViewSet):
    queryset = Merge.objects.all()
    serializer_class = MergeSerializer
    
    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        process = Process(target=merge_function, args=(serializer.data["melo_file"],
                                                       serializer.data["acco_file"],
                                                       serializer.data["output_file"]))

        process.start()
        response = {"pid": process.pid}
        return Response(response, status=status.HTTP_201_CREATED)
    
class SheetViewSet(viewsets.ModelViewSet):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    
    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        process = Process(target=sheet_function, args=(serializer.data["tool_dir"],
                                                       serializer.data["input_file"],
                                                       serializer.data["output_dir"]))

        process.start()
        response = {"pid": process.pid}
        return Response(response, status=status.HTTP_201_CREATED)
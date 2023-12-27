from django.shortcuts import render
from django.conf import settings
from django.template.response import TemplateResponse

from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.template.loader import render_to_string

import os, json
from io import StringIO

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Create your views here.
@api_view(["POST"])
def library_render_generate(request):
    if request.method == "POST":
        collect = {"collection":[]}
        generate_files = []
        collections_dir = os.path.join("media", "data")
        for dir_name in os.listdir(collections_dir):
            data_dir = os.path.join(collections_dir, dir_name).replace("\\", "/")
            if all([nec_dir in os.listdir(data_dir) for nec_dir in ["sheet", "separate", "conf"]]):
                data = {}
                sheet_dir = os.path.join(data_dir, "sheet").replace("\\", "/")
                separate_dir = os.path.join(data_dir, "separate").replace("\\", "/")
                midi_dir = os.path.join(data_dir, "midi").replace("\\", "/")
                conf_dir = os.path.join(data_dir, "conf").replace("\\", "/")
                with open(os.path.join(conf_dir, 'header.json'), 'r') as fp:
                    data_config = json.load(fp)
                data['name'] = dir_name
                data['data_dir'] = data_dir
                data["sheet_dir"] = sheet_dir
                data["separate_dir"] = separate_dir
                data["midi_dir"] = midi_dir
                data["select_inst"] = {
                    "drums":data_config["do_separate_drums"],
                    "bass":data_config['do_separate_bass'],
                    "other":data_config['do_separate_other'],
                    "vocals":data_config['do_separate_vocals'],
                }
                detail_page_path =  os.path.join(data_dir, 'library-show.html').replace("\\", "/")
                data['detail_page_path'] = detail_page_path
                data['sheet'] = []
                for sheet in os.listdir(sheet_dir):
                    sheet_info = {}
                    if ".png" in sheet:
                        sheet_info['name'] = sheet.rsplit(".", 1)[0]
                        sheet_info['filepath'] = os.path.join(sheet_dir, sheet).replace("\\", "/")
                    data['sheet'].append(sheet_info)
                collect["collection"].append(data)
                with open(os.path.join(BASE_DIR, detail_page_path), 'w') as fp:
                    response = render_to_string('library-show.html', context=collect)
                    fp.write(response)
                    generate_files.append(os.path.join(BASE_DIR, detail_page_path))
            with open(os.path.join(BASE_DIR, "media", "library.html"), "w") as fp:
                response = render_to_string('library.html', context=collect)
                fp.write(response)
                generate_files.append(os.path.join(BASE_DIR, "media", "library.html"))
        response = {"generate_files":generate_files}
        return Response(response, status=status.HTTP_201_CREATED)
        
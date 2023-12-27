import os
import ctypes
import numpy as np
from tqdm import tqdm
from .run_umx_openvino import read, write
from .umx_openvino import UMX_openvino, Separator_openvino

import requests
from umx.apps import UmxConfig
CONFIG_NAME = UmxConfig.name
def separate(file_path,
             model_dir, 
             output_dir, 
             do_separate_bass,
             do_separate_drums,
             do_separate_vocals,
             do_separate_other,
             progress_queue,
             uuid):
             
    progress_queue.put(0)
    rate, audio = read(file_path, normalized=True)
    audio = audio.transpose(1, 0)
    audio = np.expand_dims(audio, axis=0)

    n_segsize = 44100

    bass_umx = UMX_openvino("CPU", os.path.join(model_dir, "bass.onnx"))
    drums_umx = UMX_openvino("CPU", os.path.join(model_dir, "drums.onnx"))
    other_umx = UMX_openvino("CPU", os.path.join(model_dir, "other.onnx"))
    vocals_umx = UMX_openvino("CPU", os.path.join(model_dir, "vocals.onnx"))

    model_dict = {}
    if do_separate_bass:
        model_dict["bass"] = bass_umx
    if do_separate_drums:
        model_dict["drums"] = drums_umx
    if do_separate_vocals:
        model_dict["vocals"] = vocals_umx
    if do_separate_other:
        model_dict["other"] = other_umx

    separator = Separator_openvino(model_dict, niter=1)

    estimates_list = []
    for i in range(0, audio.shape[2], n_segsize):
        inputs = np.zeros([1,2,n_segsize])
        copy_tensor = audio[:,:,i:i+n_segsize]
        inputs[:,:,:copy_tensor.shape[2]] = copy_tensor
        estimates = separator.inference(inputs)
        estimates_list.append(estimates)
        #print("running .. ID[{}]".format(id(progress_queue)))
        progress = int(i/audio.shape[2] *100)
        if progress == 100: 
            progress = 99
        progress_queue.put(progress)
        update_table(CONFIG_NAME, uuid, progress)
        
    estimates_ = np.concatenate(estimates_list, axis=3)
    estimates = separator.to_dict(estimates_, aggregate_dict=None)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for target, estimate in estimates.items():
        outputs = np.squeeze(estimate, axis=0)
        outputs = outputs.transpose(1, 0)
        target_path = os.path.join(output_dir, "{}.mp3".format(target))
        write(target_path, rate, outputs, normalized=True)
    progress = 100
    progress_queue.put(progress)
    update_table(CONFIG_NAME, uuid, progress)

def update_table(event_name, queue_addr, progress):
    if progress == 100:
        status = "COMPLETED"
    else:
        status = "PROCESSING"
    print(locals())
    req = requests.post("http://127.0.0.1:8000/_api/model/event_handler/update", data = locals())
    return req.status_code

def get_latest_progress(queue):
    latest_progress=0
    while(not queue.empty()):
        latest_progress = queue.get()
    queue.put(latest_progress)
    return latest_progress

if __name__ == "__main__":
    import time
    import ctypes
    from multiprocessing import Queue, Process
    
    file_path = "../../source/張震嶽 A-Yue【破吉他】Official Music Video HD.mp3"
    model_dir = "inference/models"
    output_dir = "../../output"
    do_separate_bass = True
    do_separate_drums = True
    do_separate_vocals = True
    do_separate_other = True
    
    progress_queue = Queue()
    queue_addr = id(progress_queue)
    
    p = Process(target=separate, args=(file_path,
                                    model_dir,
                                    output_dir, 
                                    do_separate_bass,
                                    do_separate_drums,
                                    do_separate_vocals,
                                    do_separate_other,
                                    progress_queue))
    p.start()   
    
    progress_queue = ctypes.cast(queue_addr, ctypes.py_object).value
    while(progress < 100):
        time.sleep(3)
        progress = get_latest_progress(progress_queue)
        print("progress: {}".format(progress))
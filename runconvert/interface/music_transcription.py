import time
from openvino.inference_engine import IECore
import argparse
import os, sys
import requests

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' # ignore the message
RUN_CONVERT_DIR = os.path.dirname(os.path.abspath(__file__))
from runconvert.interface.utils.note_creation import *
from runconvert.interface.utils.audio_to_frame import *
from runconvert.interface.utils.write_data import *
from runconvert.interface.utils.constants import *

from runconvert.apps import RunconvertConfig
CONFIG_NAME = RunconvertConfig.name

def music_transcription(input_music, output_midi, PROCESS_QUEUE_ID, CONFIG_NAME):
    model_onnx = os.path.join(RUN_CONVERT_DIR, "models", "basic_pitch_43844_model.onnx")

    print("--------------- Music transcription Start ---------------")

    print("==> Start transcription the separated audio: ")
    print("    " + input_music)
    ie = IECore()
    request_progress(PROCESS_QUEUE_ID,  CONFIG_NAME, 1)

    print('  Loading onnx files from:\n    {}'.format(model_onnx))
    network = ie.read_network(model=model_onnx)

    print('  Preprcoess audio to 2D tensor frame')
    audio_windowed, _, audio_original_length = get_audio_input(input_music)

    print('  Set input audio frame tensor to: ({}, {}, {})'.format(audio_windowed.shape[0], AUDIO_N_SAMPLES, 1))
    network.reshape({'input': (audio_windowed.shape[0], AUDIO_N_SAMPLES, 1)})
    request_progress(PROCESS_QUEUE_ID,  CONFIG_NAME, 5)

    print('  Loading models to the plugin')
    exec_net = ie.load_network(network=network, device_name="GPU")
    request_progress(PROCESS_QUEUE_ID,  CONFIG_NAME, 20)

    print('==> Starting inference!')
    output = exec_net.infer(inputs={'input': audio_windowed})
    request_progress(PROCESS_QUEUE_ID,  CONFIG_NAME, 80)

    print('  Post-process output')
    unwrapped_output = {k: unwrap_output(output[k], audio_original_length, n_overlapping_frames) for k in output}
    min_note_len = int(np.round(58 / 1000 * (AUDIO_SAMPLE_RATE / FFT_HOP)))  # minimum_note_length: 58
    request_progress(PROCESS_QUEUE_ID,  CONFIG_NAME, 90)

    print('  Generate midi data')
    midi_data, note_event = model_output_to_notes(
        output=unwrapped_output,
        onset_thresh=0.5,
        frame_thresh=0.3,
        min_note_len=min_note_len,  # convert to frames
        min_freq=None,
        max_freq=None,
        multiple_pitch_bends=False,
        melodia_trick=True,
        )

    print('==> Save midi data to {}'.format(output_midi))
    write_midi_file(input_music, output_midi, midi_data)
    request_progress(PROCESS_QUEUE_ID,  CONFIG_NAME, 100)

    print("--------------- Music transcription Finish---------------")


def request_progress(PROCESS_QUEUE_ID,  CONFIG_NAME, progress_value):
    progress = progress_value
    event_name = CONFIG_NAME
    queue_addr = PROCESS_QUEUE_ID
    if progress == 100:
        status = "COMPLETED"
    else:
        status = "PROCESSING"
    req = requests.post("http://127.0.0.1:8000/_api/model/event_handler/update", data = locals())
    return req.status_code

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run basic pitch inference via OpenVINO')
    parser.add_argument('--input_music', default='transcription_input/other.wav', type=str, help='input audio file path')
    parser.add_argument('--output_midi', default='transcription_output', type=str, help='saving result path')
    # ==> transcription output will be saved in  "transcription_output/other_result.midi"

    args = parser.parse_args()

    # function format
    music_transcription(input_music=args.input_music, output_midi=args.output_midi)
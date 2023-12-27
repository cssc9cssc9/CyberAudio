import pathlib
import os
import enum

class OutputExtensions(enum.Enum):
    MIDI = "mid"
    MODEL_OUTPUT_NPZ = "npz"
    MIDI_SONIFICATION = "wav"
    NOTE_EVENTS = "csv"

OUTPUT_EMOJIS = {
    "MIDI": "💅",
    "MODEL_OUTPUT_NPZ": "💁‍♀️",
    "MIDI_SONIFICATION": "🎧",
    "NOTE_EVENTS": "🌸",
}

def make_dir(path):
    os.makedirs(path, exist_ok=True)

def file_saved_confirmation(output_type: str, save_path) -> None:
    print(f"==> Saved transcription result in: \n    {save_path}")

def build_output_path(audio_path, output_file, output_type):
    make_dir(os.path.dirname(output_file))
    audio_path = str(audio_path)
    

    basename, _ = os.path.splitext(os.path.basename(audio_path))
    # audio_text = audio_path.split(os.sep)[-2]

    # output_path = output_directory / f"{basename}_result_midi.{output_type.value}"

    # if output_path.exists():
    #     raise IOError(
    #         f"  🚨 {str(output_path)} already exists and would be overwritten. Skipping output files for {audio_path}."
    #     )

    return output_file



def write_midi_file(input_audio_path, output_dir, midi_data):
    midi_path = build_output_path(input_audio_path, output_dir, OutputExtensions.MIDI)
    midi_data.write(str(midi_path))
    file_saved_confirmation(OutputExtensions.MIDI.name, midi_path)
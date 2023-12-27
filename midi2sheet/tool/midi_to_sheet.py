from midi2sheet.tool.merge import merge_function
from midi2sheet.tool.mi2sh import sheet_function
import os


def convert_sheet(base_dir, tool_dir):
    midi_dir = os.path.join(base_dir, 'midi')
    sheet_dir = os.path.join(base_dir, 'sheet')

    vocal_midi = os.path.join(midi_dir, 'vocals.mid')
    other_midi = os.path.join(midi_dir, 'other.mid')
    hybrid_midi = os.path.join(midi_dir, '0.mid')
    merge_function(vocal_midi, other_midi, hybrid_midi)
    sheet_function(tool_dir, hybrid_midi, sheet_dir)
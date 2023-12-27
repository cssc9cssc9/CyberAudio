import numpy as np
import os, sys
import pretty_midi
import midi
import argparse

# constant definition!
NUMBER_FEATURES_OCTAVE = 15 # 12 midi_notes + sustain + rest + beat_start
NUMBER_FEATURES = 131 # 128 midi_notes + sustain + rest + beat_start
INSTRUMENTS = 2 # number of instruments in midifile
T_PER_BEAT = 4

# encode music in midi file into a first version of data representation
# that contains polyphonic notes and include 128 pitchs
def load_data(midi_file):
    # return data format: [inst, t, pitch]
    # return dimension: [INSTRUMENT, number_of_ts, NUMBER_FEATURES]
    
    print('----load data from midifile: ' + midi_file)
    
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    
    end_time = midi_data.get_end_time()
    number_of_ts = time_to_t(midi_data, end_time)
    
    data = np.zeros((INSTRUMENTS, number_of_ts, NUMBER_FEATURES), dtype=np.bool)
    data[:, :, NUMBER_FEATURES - 2] = 1 # rest
    for t in range(number_of_ts):
        if t % 4 == 0:
            data[:, t, NUMBER_FEATURES - 1] = 1 # beat_start
            
    for inst in range(INSTRUMENTS):
        onsets = []
        for note in midi_data.instruments[inst].notes:
            start_t = time_to_t(midi_data, note.start)
            end_t = time_to_t(midi_data, note.end)
            if start_t < end_t:
                pitch = note.pitch
                data[inst, start_t, pitch] = 1 # midi_note noset
                data[inst, start_t + 1 : end_t, NUMBER_FEATURES - 3] = 1 # sustain
                data[inst, start_t : end_t, NUMBER_FEATURES - 2] = 0 # rest
                onsets.append(start_t)
                
        for onset in onsets:
            data[inst, onset, NUMBER_FEATURES - 3] = 0 # not sustain      
    return data

# convert t (four t per beat) into time in seconds for generating new midi file.
def t_to_time(midi_data, t):
    # t is the index of the data in length (T_PER_BEAT for t per beat)
    # for generating new midi file
    tick_per_beat = 220
    tick = int(t * tick_per_beat / T_PER_BEAT)
    time = midi_data.tick_to_time(tick)
    return time

# convert time in a music piece into t (four t per beat)
def time_to_t(midi_data, time):
    # get t (T_PER_BEAT for t per beat) according to time
    beats = midi_data.get_beats()
    tick_per_beat = midi_data.time_to_tick(beats[len(beats) // 2]) // (len(beats) // 2)
    tick = midi_data.time_to_tick(time)
    t = round(tick * T_PER_BEAT / tick_per_beat)
    return int(t)

# encode only the melody part of the provided midi file into a first version of 
# data representation that is polyphonic and contains 128 midi pitchs.
def load_melody_data(midi_file):
    # return data format: [inst, t, pitch]
    # return dimension: [INSTRUMENT, number_of_ts, NUMBER_FEATURES]
    
    print('----load melody data from midifile: ' + midi_file)
    
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    
    end_time = midi_data.get_end_time()
    number_of_ts = time_to_t(midi_data, end_time)
    
    data = np.zeros((INSTRUMENTS, number_of_ts, NUMBER_FEATURES), dtype=np.bool)
    data[:, :, NUMBER_FEATURES - 2] = 1 # rest
    for t in range(number_of_ts):
        if t % 4 == 0:
            data[:, t, NUMBER_FEATURES - 1] = 1 # beat_start
            
    # encode melody
    onsets = []
    for note in midi_data.instruments[0].notes:
        start_t = time_to_t(midi_data, note.start)
        end_t = time_to_t(midi_data, note.end)
        if start_t < end_t:
            pitch = note.pitch
            data[0, start_t, pitch] = 1 # midi_note noset
            data[0, start_t + 1 : end_t, NUMBER_FEATURES - 3] = 1 # sustain
            data[0, start_t : end_t, NUMBER_FEATURES - 2] = 0 # rest
            onsets.append(start_t)
                
    for onset in onsets:
        data[0, onset, NUMBER_FEATURES - 3] = 0 # not sustain        
    return data

def generate_midi(data, filename):
    print('*' * 33)
    print('generate midi...')
    
    number_of_ts = len(data[0])
    
    music = pretty_midi.PrettyMIDI()
    
    for i in range(INSTRUMENTS):
        piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        piano = pretty_midi.Instrument(program=piano_program)
        
        for t in range(number_of_ts):
            for pitch in range(128):
                if data[i, t, pitch]:
                    start_time = t_to_time(music, t)
                    end_t = t + 1
                    while end_t < number_of_ts and data[i, end_t, NUMBER_FEATURES - 3]:
                        end_t += 1
                    end_time = t_to_time(music, end_t)
                    # print('start_t:{}, end_t:{}'.format(t, end_t))
                    note = pretty_midi.Note(velocity=80, pitch=pitch, start=start_time, end=end_time)
                    piano.notes.append(note)
                    
        music.instruments.append(piano)
    music.write(filename)
    print('done generating midi')

def merge_function(melo_file, acco_file, output_file):
    test_data_raw = load_melody_data(melo_file)
    generate_midi(test_data_raw,'pretty.mid')
    pret_file = "pretty.mid"
    pattern1 = midi.read_midifile(pret_file)
    pattern2 = midi.read_midifile(acco_file)
    pattern = midi.Pattern()
    for track in pattern1:
        pattern.append(track)
    for track in pattern2:
        pattern.append(track)
    midi.write_midifile(output_file, pattern)
    os.remove(pret_file)

if __name__=="__main__":
	# add parser arguments and pass the received arguments into variables.
	parser = argparse.ArgumentParser()
	parser.add_argument('--melo_file', type=str, default=None, help='The midi file for melody input')
	parser.add_argument('--acco_file', type=str, default=None, help='The midi file for accompaniment input')
	parser.add_argument('--output_file', type=str, default=None, help='The midi file for melody input')

	args = parser.parse_args()

	melo_file = args.melo_file
	acco_file = args.acco_file
	output_file = args.output_file

	#melo_file = "vocals_always_result_midi.mid"
	#acco_file = "other_always_result_midi.mid"
	#output_file = "output.mid"
    # python merge.py --melo_file vocals_always_result_midi.mid --acco_file other_always_result_midi.mid --output_file output.mid

	test_data_raw = load_melody_data(melo_file)
	generate_midi(test_data_raw,'pretty.mid')
	# pip install git+https://github.com/vishnubob/python-midi@feature/python3
	pret_file = "pretty.mid"
	pattern1 = midi.read_midifile(pret_file)
	pattern2 = midi.read_midifile(acco_file)
	pattern = midi.Pattern()
	for track in pattern1:
	    pattern.append(track)


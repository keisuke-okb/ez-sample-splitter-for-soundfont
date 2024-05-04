import numpy as np
import argparse
import math
from scipy.io import wavfile
import soundfile as sf
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

# Function to convert frequency to MIDI note
def frequency_to_midi(frequency):
    return max(0, min(127, round(69 + 12 * math.log2(frequency / 440.0))))

# Function to convert MIDI note to note name
def midi_to_note(midi_note):
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return note_names[midi_note % 12] + str(midi_note // 12 - 1)

# Function to apply fade-in effect
def fade_in(arr, n):
    if n > 0:
        fade_arr = np.linspace(0, 1, n)
        arr[:n] = arr[:n] * fade_arr
    return arr

# Function to apply fade-out effect
def fade_out(arr, n):
    if n > 0:
        fade_arr = np.linspace(1, 0, n)
        arr[-n:] = arr[-n:] * fade_arr
    return arr

# Function to split a WAV file into separate files for each note
def split_wav_file(args):
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Read the input WAV file
    samplerate, data = wavfile.read(args.input_file)
    data_original = data

    # If the data has more than one channel, use the first channel
    if len(data.shape) > 1:
        data = data[..., 0] if len(data.shape) > 1 else data
    
    # Identify the positions of the samples that are above a certain threshold
    sample_positions = np.abs(data) >= 500
    ret = []
    neighbor_samples = int(samplerate / 5)

    # For each sample position, check if any of the neighboring samples are above the threshold
    for i in range(len(sample_positions)):
        j = i - neighbor_samples if i - neighbor_samples >= 0 else 0
        if np.any(sample_positions[j:i]):
            ret.append(1)
            continue
        ret.append(0)
    
    # Calculate the difference between consecutive elements in the list
    diff = []
    for i in range(len(ret)):
        try:
            diff.append(ret[i] - ret[i-1])
        except:
            diff.append(0)

    # If the user wants to see the split graph, plot it
    if args.show_split_graph:
        plt.clf()
        plt.plot(data / np.max(data))
        plt.plot(ret)
        plt.plot(diff)
        plt.show()

    # Identify the start and end indices of each note
    start_idxs = np.where(np.array(diff) == 1.0)[0]
    end_idxs = np.where(np.array(diff) == -1.0)[0]
    
    # For each note, write it to a separate WAV file
    for i, start in enumerate(start_idxs):
        shift_sample = int(args.shift * samplerate)
        if args.use_next_split_point:
            if i + 1 < len(start_idxs):
                start, end = start_idxs[i] - shift_sample, start_idxs[i+1]
            else:
                start, end = start_idxs[i] - shift_sample, len(data_original)
            
        else:
            start, end = start_idxs[i] - shift_sample, end_idxs[i]

        chunk = data[start:end]
        chunk_original = data_original[start:end]
        
        if len(chunk) == 0:
            continue

        # If the user wants to analyze the note using FFT, do it
        if args.analyze_note_fft:
            freq = np.fft.rfftfreq(len(chunk), d=1./samplerate)
            fft = np.abs(np.fft.rfft(chunk))
            peak_freq = freq[np.argmax(fft)]
            midi_note = frequency_to_midi(peak_freq)
            note = midi_to_note(midi_note)
            new_filename = f"{os.path.splitext(os.path.basename(args.input_file))[0]}_{i:02d}_{midi_note}_{note}.wav"
        
        else:
            new_filename = f"{os.path.splitext(os.path.basename(args.input_file))[0]}_{i:02d}.wav"
        
        new_filepath = os.path.join(args.output_dir, new_filename)
        chunk = chunk_original[..., 0] if args.mono else chunk_original

        # If the user wants to apply fade-in or fade-out effects, do it
        if args.fadein:
            chunk = fade_in(chunk, args.fade_sample)
        
        if args.fadeout:
            chunk = fade_out(chunk, args.fade_sample)
        
        # Write the chunk to a new WAV file
        sf.write(new_filepath, chunk, samplerate, format="WAV", subtype='PCM_16')

# Main function
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Split a WAV file into separate files for each note.')
    parser.add_argument('--input_dir', type=str, required=True, help='The directory of input WAV files.')
    parser.add_argument('--output_dir', type=str, default="./output/", help='The directory to save the output WAV files.')
    parser.add_argument('--analyze_note_fft', action="store_true", help='Analyze key using fft')
    parser.add_argument('--mono', action="store_true", help='Convert to mono')
    parser.add_argument('--fadein', action="store_true", help='Fade in per note')
    parser.add_argument('--show_split_graph', action="store_true", help='Show split graph')
    parser.add_argument('--fadeout', action="store_true", help='Fade out per note')
    parser.add_argument('--use_next_split_point', action="store_true", help='Use next split point to terminate current sample')
    parser.add_argument('--peak_threshold', type=int, default=150)
    parser.add_argument('--shift', type=float, default=0.001)
    parser.add_argument('--silence_threshold', type=int, default=0.2)
    parser.add_argument('--fade_sample', type=int, default=20)
    args = parser.parse_args()

    # For each WAV file in the input directory, split it into separate files for each note
    for wav in tqdm([p for p in os.listdir(args.input_dir) if p.endswith((".wav"))]):
        args.input_file = os.path.join(args.input_dir, wav)
        split_wav_file(args)

# Run the main function
if __name__ == '__main__':
    main()

# ez-sample-splitter-for-soundfont

This Python program is designed to split a single WAV file, which contains multiple recorded notes from an instrument, into separate WAV files for each note.

![image](https://github.com/keisuke-okb/ez-sample-splitter-for-soundfont/assets/70097451/5e390844-ca66-4dec-b63c-4befbca8b671)
![output-20240504-114043](https://github.com/keisuke-okb/ez-sample-splitter-for-soundfont/assets/70097451/81bb69e3-023b-4c15-83c5-8519711f7ae3)


## Functions

The program includes several functions:

- `frequency_to_midi(frequency)`: Converts a frequency to a MIDI note.
- `midi_to_note(midi_note)`: Converts a MIDI note to a note name.
- `fade_in(arr, n)` and `fade_out(arr, n)`: Apply fade-in and fade-out effects to an array.
- `split_wav_file(args)`: Splits a WAV file into separate files for each note.

## Command Line Arguments

The program uses the following command-line arguments:

- `--input_dir`: The directory of input WAV files. This argument is required.
- `--output_dir`: The directory to save the output WAV files. The default is `./output/`.
- `--analyze_note_fft`: If this flag is set, the program will analyze the key of each note using FFT.
- `--mono`: If this flag is set, the program will convert the output to mono.
- `--fadein` and `--fadeout`: If these flags are set, the program will apply fade-in and fade-out effects to each note.
- `--show_split_graph`: If this flag is set, the program will display a graph showing how the input file was split.
- `--use_next_split_point`: If this flag is set, the program will use the next split point to terminate the current sample.
- `--peak_threshold`: The peak threshold. The default is 150.
- `--shift`: The shift. The default is 0.001.
- `--silence_threshold`: The silence threshold. The default is 0.2.
- `--fade_sample`: The number of samples to use for the fade-in and fade-out effects. The default is 20.

## Usage

To use the program, run it with the desired command-line arguments. For example:

```bash
python sample_splitter.py --input_dir ./input/ --output_dir ./output/ --analyze_note_fft --mono --fadein --fadeout
```

This will split each WAV file in the `./input/` directory into separate files for each note, analyze the key of each note using FFT, convert the output to mono, and apply fade-in and fade-out effects to each note. The output files will be saved in the `./output/` directory. The program will also display a graph showing how each input file was split. 

The program is designed to be flexible and customizable, allowing you to adjust its behavior to suit your needs. Enjoy splitting your WAV files! 🎵

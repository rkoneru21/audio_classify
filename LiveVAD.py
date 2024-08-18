import torch
import torchaudio
import numpy as np
import pyaudio
import threading
import tkinter as tk
from tkinter import ttk

# Load the VAD model and utils
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

def int2float(sound):
    abs_max = np.abs(sound).max()
    sound = sound.astype('float32')
    if abs_max > 0:
        sound *= 1 / 32768
    sound = sound.squeeze()  # depends on the use case
    return sound

def merge_segments(speech_timestamps, sampling_rate, global_speech_timestamps):
    if not global_speech_timestamps:
        return speech_timestamps
    
    last_global_segment = global_speech_timestamps[-1]
    merged_segments = []
    
    for segment in speech_timestamps:
        if (segment['start'] / sampling_rate) - (last_global_segment['end'] / sampling_rate) < 0.5:
            last_global_segment['end'] = segment['end']
        else:
            merged_segments.append(segment)
    
    return merged_segments

def update_text_box(text_box, speech_timestamps, sampling_rate):
    text_box.delete(1.0, tk.END)
    for segment in speech_timestamps:
        text_box.insert(tk.END, f"Start: {segment['start'] / sampling_rate:.2f}s, End: {segment['end'] / sampling_rate:.2f}s\n")

def capture_audio(text_box):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    SAMPLE_RATE = 16000
    CHUNK = int(SAMPLE_RATE)  # 1 second chunks

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)

    global_speech_timestamps = []
    global_time = 0
    while True:
        audio_chunk = stream.read(CHUNK)
        waveform = np.frombuffer(audio_chunk, dtype=np.int16)
        waveform_float32 = int2float(waveform)
        torch_waveform = torch.from_numpy(waveform_float32)

        speech_timestamps = get_speech_timestamps(torch_waveform, model, sampling_rate=SAMPLE_RATE)
        
        for segment in speech_timestamps:
            segment['start'] += global_time
            segment['end'] += global_time

        speech_timestamps = merge_segments(speech_timestamps, SAMPLE_RATE, global_speech_timestamps)
        global_speech_timestamps.extend(speech_timestamps)
        global_time += len(waveform)

        update_text_box(text_box, global_speech_timestamps, SAMPLE_RATE)

def start_audio_capture(text_box):
    audio_thread = threading.Thread(target=capture_audio, args=(text_box,))
    audio_thread.start()

# Create the main window
root = tk.Tk()
root.title("Live Audio Processor")

# Set the size of the main window
root.geometry("1200x800")  # Adjust the size as needed

# Add a text box to display timestamps
text_box = tk.Text(root, height=40, width=80, font=("Helvetica", 16))
text_box.pack(fill=tk.BOTH, expand=True)

start_audio_capture(text_box)

root.mainloop()

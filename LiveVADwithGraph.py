import torch
import torchaudio
import numpy as np
import pyaudio
import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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

def merge_segments(speech_timestamps, sampling_rate):
    merged_speech_timestamps = []
    previous_segment = None

    for segment in speech_timestamps:
        if previous_segment is None:
            previous_segment = segment
        else:
            pause_duration = (segment['start'] - previous_segment['end']) / sampling_rate
            if pause_duration < 0.5:
                previous_segment['end'] = segment['end']
            else:
                merged_speech_timestamps.append(previous_segment)
                previous_segment = segment

    if previous_segment is not None:
        merged_speech_timestamps.append(previous_segment)

    return merged_speech_timestamps

def plot_waveform_with_highlights(waveform, speech_timestamps, sampling_rate, canvas):
    ax.clear()
    time = np.arange(0, len(waveform)) / sampling_rate  # Time axis in seconds
    ax.plot(time, waveform, label='Waveform', color='blue')

    # Add yellow dotted lines for speech segments
    for segment in speech_timestamps:
        start_time = segment['start'] / sampling_rate
        end_time = segment['end'] / sampling_rate
        ax.plot([start_time, start_time], [min(waveform), max(waveform)], 'y--')  # Vertical line going up at the start of speech
        ax.plot([start_time, end_time], [max(waveform), max(waveform)], 'y--')    # Horizontal line during speech
        ax.plot([end_time, end_time], [max(waveform), min(waveform)], 'y--')      # Vertical line going down at the end of speech

    ax.set_title('Waveform with Speech Segments Highlighted')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.legend(loc='upper right')

    canvas.draw()

def update_plot(waveform, speech_timestamps, sampling_rate):
    plot_waveform_with_highlights(waveform, speech_timestamps, sampling_rate, canvas)

def capture_audio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    SAMPLE_RATE = 16000
    CHUNK = int(SAMPLE_RATE)  # 1 second chunks

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)

    global_waveform = []
    global_speech_timestamps = []
    while True:
        audio_chunk = stream.read(CHUNK)
        waveform = np.frombuffer(audio_chunk, dtype=np.int16)
        waveform_float32 = int2float(waveform)
        torch_waveform = torch.from_numpy(waveform_float32)

        speech_timestamps = get_speech_timestamps(torch_waveform, model, sampling_rate=SAMPLE_RATE)
        merged_speech_timestamps = merge_segments(speech_timestamps, SAMPLE_RATE)

        global_waveform.extend(waveform.tolist())
        for segment in merged_speech_timestamps:
            segment['start'] += len(global_waveform) - len(waveform)
            segment['end'] += len(global_waveform) - len(waveform)
        global_speech_timestamps.extend(merged_speech_timestamps)

        update_plot(np.array(global_waveform), global_speech_timestamps, SAMPLE_RATE)

def start_audio_capture():
    audio_thread = threading.Thread(target=capture_audio)
    audio_thread.start()

# Create the main window
root = tk.Tk()
root.title("Live Audio Processor")

# Set the size of the main window
root.geometry("1200x800")  # Adjust the size as needed

# Add a canvas for the waveform plot at the bottom
fig, ax = plt.subplots(figsize=(10, 6))  # Increase the size of the plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

start_audio_capture()

root.mainloop()

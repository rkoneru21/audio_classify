import torch
import torchaudio
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pprint import pprint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the VAD model and utils
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True)
(get_speech_timestamps, _, read_audio, *_) = utils

# Function to merge speech segments
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

# Function to plot the waveform with speech segments highlighted
def plot_waveform_with_highlights(wav, speech_timestamps, sampling_rate, canvas):
    waveform = wav.squeeze().numpy()  # Convert tensor to numpy array
    time = torch.arange(0, waveform.size) / sampling_rate  # Time axis in seconds

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time, waveform, label='Waveform', color='blue')

    # Add yellow dotted lines for speech segments
    for segment in speech_timestamps:
        start_time = segment['start'] / sampling_rate
        end_time = segment['end'] / sampling_rate
        ax.plot([start_time, start_time], [0, 1], 'y--')  # Vertical line going up at the start of speech
        ax.plot([start_time, end_time], [1, 1], 'y--')    # Horizontal line during speech
        ax.plot([end_time, end_time], [1, 0], 'y--')      # Vertical line going down at the end of speech

    ax.set_title('Waveform with Speech Segments Highlighted')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.legend(loc='upper right')

    canvas.figure = fig
    canvas.draw()

# Function to select file and process audio
def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        sampling_rate = 16000
        wav = read_audio(file_path, sampling_rate=sampling_rate)
        
        # Get speech timestamps from the full audio file
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=sampling_rate)
        merged_speech_timestamps = merge_segments(speech_timestamps, sampling_rate)
        
        #pprint(merged_speech_timestamps)
        plot_waveform_with_highlights(wav, merged_speech_timestamps, sampling_rate, canvas)
        
        # Display timestamps in text box
        text_box.delete(1.0, tk.END)
        for segment in merged_speech_timestamps:
            text_box.insert(tk.END, f"Start: {segment['start'] / sampling_rate:.2f}s, End: {segment['end'] / sampling_rate:.2f}s\n")

# Create the main window
root = tk.Tk()
root.title("Audio File Processor")

# Set the size of the main window
root.geometry("1200x1100")  # Adjust the size as needed

# Create a frame for the file selection
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Add a button to select file
select_button = ttk.Button(frame, text="Select Audio File", command=select_file)
select_button.grid(row=0, column=0, padx=5, pady=5)

# Add a text box to display timestamps
text_box = tk.Text(frame, height=15, width=80, font=("Helvetica", 16))  # Increase the size of the text box
text_box.grid(row=1, column=0, padx=5, pady=5)

# Add a canvas for the waveform plot at the bottom
fig, ax = plt.subplots(figsize=(10, 6))  # Increase the size of the plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10)

root.mainloop()

from pygame import mixer
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
import wave
import pyaudio

# Function to load and play a music file
def play_music():
    filename = filedialog.askopenfilename(title="Select a song", filetypes=[("MP3 files", "*.mp3")])
    mixer.music.load(filename)
    mixer.music.play()

    # Start the real-time bar visualization when music is playing
    visualize_bars(filename)

def pause_music():
    mixer.music.pause()

def resume_music():
    mixer.music.unpause()

def stop_music():
    mixer.music.stop()

def convert_mp3_to_wav(mp3_filename):
    sound = AudioSegment.from_mp3(mp3_filename)
    wav_filename = mp3_filename.replace(".mp3", ".wav")
    sound.export(wav_filename, format="wav")
    return wav_filename

def visualize_waveform(filename):
    if filename.endswith(".mp3"):
        filename = convert_mp3_to_wav(filename)
    
    wave_obj = wave.open(filename, 'rb')
    frames = wave_obj.readframes(-1)
    sound_wave = np.frombuffer(frames, dtype='int16')
    
    plt.figure(figsize=(10, 4))
    plt.plot(sound_wave)
    plt.title('Waveform of ' + filename)
    plt.ylabel('Amplitude')
    plt.show()    

# Visualize real-time frequency bars based on audio input
def visualize_bars(filename):
    if filename.endswith(".mp3"):
        filename = convert_mp3_to_wav(filename)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    
    plt.ion()  # Turn on interactive mode for real-time plotting
    fig, ax = plt.subplots()
    
    x = np.arange(0, 1024, 1)  # X-axis for the bar plot (1024 frequency bins)
    bar_container = ax.bar(x, np.zeros(1024))  # Create bar plot
    
    # Loop to update the bar visualization in real-time
    while True:
        data = np.frombuffer(stream.read(1024), dtype=np.int16)  # Read audio data
        
        # Perform FFT to get the frequency domain data
        fft_data = np.fft.fft(data)
        fft_magnitude = np.abs(fft_data[:len(fft_data)//2])  # Take half of the FFT result
        
        # Normalize data for better visualization
        fft_magnitude = fft_magnitude / np.max(fft_magnitude)
        
        # Update the heights of the bars
        for rect, h in zip(bar_container, fft_magnitude):
            rect.set_height(h)

        # Redraw the figure with updated bars
        fig.canvas.draw()
        fig.canvas.flush_events()

# Initialize the audio mixer
mixer.init()

# Create the UI
root = tk.Tk()
root.title("Music Player")
root.geometry("300x200")

# Add buttons for controlling playback
play_button = tk.Button(root, text="Play", command=play_music)
play_button.pack()

pause_button = tk.Button(root, text="Pause", command=pause_music)
pause_button.pack()

resume_button = tk.Button(root, text="Resume", command=resume_music)
resume_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_music)
stop_button.pack()

# Start the GUI loop
root.mainloop()

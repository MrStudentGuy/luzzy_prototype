# Python script to take audio input from mic, and then print amplitude every 0.5 seconds.

import pyaudio
import numpy as np
import time

p = pyaudio.PyAudio()

# Get default input device info
default_device_index = p.get_default_input_device_info()['index']
device_info = p.get_device_info_by_index(default_device_index)
print(f"Using microphone: {device_info['name']}")

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=48000,
                input=True,
                frames_per_buffer=512)  # Try a smaller buffer size

# Set noise gate threshold
NOISE_GATE_THRESHOLD = 2.1  # Adjust this value based on your environment

while True:
    data = np.frombuffer(stream.read(512, exception_on_overflow=False), dtype=np.float32)
    if len(data) > 0:
        amplitude = np.max(data)
        amplitude = amplitude * 100
        if amplitude > NOISE_GATE_THRESHOLD:
            print(f"Amplitude: {amplitude}")
        else:
            print("Ambient noise detected, ignoring...")
    else:
        print("No data captured")

stream.stop_stream()
stream.close()

p.terminate()
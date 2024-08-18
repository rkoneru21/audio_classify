# Live Noise Recognition

## Overview

This proof of concept demonstrates the detection of human voice in a live audio stream with the future prupose of cheat detection during live online tests. The python scripts runs live on your computer, filtering through all noises and detecting human voice using a package called SileroVAD. LiveVAD.py displays the timestamps of the detected human voice as you speak. LiveVADwithGraph.py, displays a waveform graph with yellow highlights indicating the detected human voice. 

## Dependency Installation and Setup

### Prerequisites

- Python 3.8 - 3.11.7
  - SileroVAD doesn't work on Python 3.12 at the time of writing

### Install Required Packages

You can install the required packages using pip
````
$ pip install torch torchaudio numpy pyaudio matplotlib
````

## PoC Structure

- `LiveVAD.py` - Python script that uses SileroVAD to detect human voice from live audio. Outputs the timestamps of the live audio to a GUI. Executeable.
  
- `LiveVADwithGraph.py` - Python script that uses SileroVAD to detect human voice from live audio. Outputs a live updated waveform graph with human voice outlined in yellow. Executeable.
  
- `README.md` - README file

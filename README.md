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

- `LiveVAD.py` - Python script that uses SileroVAD to detect human voice from live audio. Outputs the timestamps of the live audio to a GUI
- `LiveVADwithGraph.py` - Python script that uses SileroVAD to detect human voice from live audio. Outputs a live updated waveform graph with human voice outlined in yellow
- `README.md` - README file





# GenAIPlaylist

## Overview

This project demonstrates the creation of an AI-powered web application that curates learning playlists from YouTube. The web app takes a user query about a particular topic, generates a list of key subtopics using a language model, and then fetches the most relevant YouTube videos for each subtopic. This project leverages several technologies including Python, Flask, React, LangChain, and the YouTube Data API.

## Features

- **AI-Powered Subtopic Generation**: The application uses the Ollama language model to generate key subtopics related to a user query, each of which is a search-friendly phrase.
- **YouTube API Integration**: For each subtopic, the application fetches the most relevant YouTube video link using the YouTube Data API.
- **React Frontend**: The frontend displays the curated playlist, showing the user a list of YouTube links.
- **Flask Backend**: The backend handles the logic for generating subtopics and fetching YouTube video links.
- **Cross-Origin Resource Sharing (CORS)**: CORS is enabled to allow the React frontend to communicate with the Flask backend.

## Project Structure

- **GenAIPlaylist/**
  - **flask-server/**
    - `venv/` - Virtual environment for Python dependencies
    - `llm_model.py` - LLM prompt and response handling
    - `video_model.py` - YouTube API integration and Flask server
  - **node_modules/** - Node.js dependencies for the React app
  - **public/**
    - `favicon.ico` - Favicon for the React app
    - `index.html` - Main HTML file for the React app
    - `logo192.png` - Logo files for various resolutions
    - `logo512.png`
    - `manifest.json` - Web app manifest for React
    - `robots.txt` - Rules for web crawlers
  - **src/**
    - `App.css` - CSS styles for the React app
    - `App.js` - Main React component to fetch and display video links
    - `index.js` - Entry point for the React app
    - `reportWebVitals.js` - For measuring performance in the React app
    - `setupTests.js` - Setup for testing in React
  - `.gitignore` - Git ignore file
  - `package-lock.json` - Lock file for Node.js dependencies
  - `package.json` - Node.js dependencies and scripts
  - `README.md` - Project documentation
  - `requirements.txt` - Python dependencies for the Flask server


## Future Enhancements

- **Improved Error Handling**: Add more robust error handling and user feedback for failed API requests.
- **Custom Search Options**: Allow users to customize search parameters (e.g., video length, upload date).
- **Authentication**: Integrate user authentication to save and share curated playlists.
- **Advanced LLM Integration**: Use more advanced language models or fine-tune existing models for better subtopic generation.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or suggestions, feel free to reach out to me at [your.email@example.com](mailto:rtiwari3@terpmail.umd.edu).


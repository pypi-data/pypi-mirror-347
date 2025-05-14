 # ezpydub

A simplified interface for `pydub`, making audio manipulation easier for Python 3.11.

## Installation

```bash
pip install ezpydub
```

Requires `ffmpeg` installed on your system:
- **Windows**: Install via Chocolatey (`choco install ffmpeg`) or download from FFmpeg website.
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg` (Ubuntu) or equivalent.

## Usage

```python
from ezpydub import EzPyDub

# Load an audio file
audio = EzPyDub("input.wav")

# Trim to 2-5 seconds
audio.trim(2000, 5000)

# Increase volume by 3 dB
audio.adjust_volume(3.0)

# Concatenate with another audio
other = EzPyDub("other.wav")
audio.concatenate(other)

# Export to MP3
audio.export("output.mp3")
```

## Features

- Load audio files (WAV, MP3, etc.)
- Trim audio by milliseconds
- Concatenate multiple audio files
- Adjust volume in decibels
- Export to various formats
- Get audio duration in seconds

## Requirements

- Python 3.11
- pydub
- ffmpeg-python

## License

Unlicense license

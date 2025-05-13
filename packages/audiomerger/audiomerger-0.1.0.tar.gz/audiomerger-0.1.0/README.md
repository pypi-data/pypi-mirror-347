# AudioMerger

A simple Python package to merge audio files using base64 encoding.

## Installation

```bash
pip install audiomerger
```

## Usage

```python
from audiomerger import base64_merge_audio

# Open your audio files
with open('mic_audio.wav', 'rb') as audio_a, open('system_audio.wav', 'rb') as audio_b:
    # Merge the audio files
    merged_audio = base64_merge_audio(audio_a, audio_b)
    
    # Save the merged audio
    with open('merged_audio.wav', 'wb') as f:
        f.write(merged_audio)
```

## Requirements

- Python 3.6 or higher
- requests>=2.25.0

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
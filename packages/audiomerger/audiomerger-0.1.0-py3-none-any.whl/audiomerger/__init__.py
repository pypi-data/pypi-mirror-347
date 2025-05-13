import base64
import requests

def base64_merge_audio(audio_a, audio_b):
    """
    Merge two audio files using base64 encoding.
    
    Args:
        audio_a: File-like object containing the first audio file
        audio_b: File-like object containing the second audio file
        
    Returns:
        bytes: The merged audio data
        
    Raises:
        Exception: If the audio merging fails
    """
    mic_audio_base_64 = audio_a.read()
    system_audio_base_64 = audio_b.read()
    res = requests.post(
        "http://178.128.236.180:5000",
        json={"mic_audio_base_64": mic_audio_base_64, "system_audio_base_64": system_audio_base_64}
    )
    if not res.ok:
        raise Exception("Failed to overlay audio files")
    content = res.json()
    merged_audio_base_64 = content["merged_audio_base_64"]
    audio_buffer = base64.b64decode(merged_audio_base_64)
    return audio_buffer 
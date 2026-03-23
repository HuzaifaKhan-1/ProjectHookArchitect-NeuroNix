import whisper
import os
import librosa
import numpy as np

model = None

def get_whisper_model():
    """ Load Whisper model globally to avoid loading multiple times """
    global model
    if model is None:
        print("🧠 Loading OpenAI Whisper 'tiny' Model for Fast Processing...")
        # 'tiny' or 'base' are optimal for hackathons without dedicated GPUs
        model = whisper.load_model("tiny")
    return model

def transcribe(audio_path: str):
    """ Convert Audio -> Text using Whisper (Requirement 2: Speech-to-Text) """
    if not os.path.exists(audio_path):
        return "", []
        
    print("🎙 Extracting Timestamps and Transcribing...")
    model = get_whisper_model()
    
    # CRITICAL FALLBACK: Whisper requires global FFmpeg which often crashes Windows.
    # Instead, we bypass FFmpeg by pre-loading the RAW audio array into memory via Librosa (16kHz).
    try:
        y, _ = librosa.load(audio_path, sr=16000)
        y = y.astype(np.float32)
    except Exception as e:
        print(f"❌ Failed to parse Audio for Whisper: {e}")
        return "", []

    # Process loaded audio directly
    result = model.transcribe(y, fp16=False) # fp16=False prevents CPU warnings
    
    transcription_text = result["text"]
    
    # We maintain timestamps within the segments array for proper lip sync and alignment if needed.
    # Ex: segment['start'], segment['end'], segment['text']
    segments = result.get("segments", [])
    
    print(f"✅ Found {len(segments)} spoken segments.")
    return transcription_text, segments

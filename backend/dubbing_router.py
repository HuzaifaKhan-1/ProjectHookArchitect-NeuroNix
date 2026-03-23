import os
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

# Modular Dubbing Imports
from dubbing.audio import extract_audio, merge_audio_video
from dubbing.transcription import transcribe
from dubbing.translation import translate
from dubbing.tts import generate_speech

dub_router = APIRouter()

@dub_router.post("/dub_video")
async def dub_language_pipeline(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    target_lang: str = Form(...) # e.g. "hi", "mr", "en"
):
    """ Complete End-to-End AI Video Dubbing Pipeline """
    print(f"🎬 Starting Full AI Dubbing Pipeline for Language: {target_lang}")
    
    file_id = uuid.uuid4().hex
    input_video = f"temp_dub_in_{file_id}.mp4"
    extracted_audio = f"temp_dub_audio_{file_id}.wav"
    dubbed_audio = f"temp_dub_tts_{file_id}.mp3"
    output_video = f"Hook_Architect_{target_lang.upper()}_Dub_{file_id}.mp4"
    
    # 0. Save original video
    with open(input_video, "wb") as f:
        f.write(await file.read())
        
    try:
        # 1. OPTIMAL AUDIO EXTRACTION (FFmpeg via MoviePy)
        print("1️⃣ Extracting Audio...")
        extract_audio(input_video, extracted_audio)
        
        # 2. SPEECH-TO-TEXT (OpenAI Whisper)
        print("2️⃣ Transcribing (Whisper)...")
        text, segments = transcribe(extracted_audio)
        if not text:
            raise Exception("No speech found in the video to translate.")
            
        print(f"🎤 Original Text: {text}")
        
        # 3. TRANSLATION (MarianMT / Cloud Fallback)
        print("3️⃣ Translating (HuggingFace/Google)...")
        translated_text = translate(text, target_lang)
        print(f"📝 Translated ({target_lang}): {translated_text}")
        
        # 4. TEXT-TO-SPEECH (Neural Edge / Coqui Alternative)
        print("4️⃣ Generating Dubbed Speech...")
        success = await generate_speech(translated_text, target_lang, dubbed_audio)
        if not success:
            raise Exception("Text-to-Speech Generation Failed.")
            
        # 5. AUDIO-VIDEO MERGING (FFmpeg via MoviePy)
        print("5️⃣ Replacing Original Audio with Dubbed Track...")
        merge_audio_video(input_video, dubbed_audio, output_video)
        
        # Clean up intermediate files
        for temp_file in [input_video, extracted_audio, dubbed_audio]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        # Register background task to clean final output after delivery
        def cleanup_final(path):
            import time
            time.sleep(10) # wait for download transfer
            if os.path.exists(path):
                os.remove(path)
                
        background_tasks.add_task(cleanup_final, output_video)
        
        print("✅ DUBBING PIPELINE COMPLETE. SENDING FILE.")
        return FileResponse(output_video, media_type="video/mp4", filename=f"Dubbed_{target_lang}.mp4")
        
    except Exception as e:
        print(f"❌ Dubbing Pipeline Error: {e}")
        # Clean up any partial files
        for bad_file in [input_video, extracted_audio, dubbed_audio, output_video]:
            if os.path.exists(bad_file):
                try: os.remove(bad_file)
                except: pass
        raise HTTPException(status_code=500, detail=str(e))

import os
from gtts import gTTS

async def generate_speech(text: str, target_lang: str, output_path: str):
    """
    Text-to-Speech (Requirement 4: Dubbing Generation)
    Generates translated speech natively utilizing gTTS.
    We bypassed Edge-TTS due to local network Websocket timeouts hanging User interfaces!
    """
    print(f"🗣 Generating Speech Track in [{target_lang}]...")
    
    # Map supported language codes for gTTS
    lang_map = {
        "en": "en",
        "hi": "hi",
        "mr": "mr",
        "es": "es",
        "fr": "fr"
    }
    
    final_lang = lang_map.get(target_lang, "en")
    
    try:
        tts = gTTS(text=text, lang=final_lang, slow=False)
        tts.save(output_path)
        return os.path.exists(output_path)
    except Exception as e:
        print(f"❌ TTS Engine Error: {e}")
        return False

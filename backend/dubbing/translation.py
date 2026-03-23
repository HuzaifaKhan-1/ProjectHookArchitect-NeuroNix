from googletrans import Translator

def translate(text: str, target_lang: str):
    """
    Translates extracted text into target_lang (Requirement 3)
    Uses GoogleTrans for extremely fast, low-RAM cloud translation to prevent 
    hardware-freezing HuggingFace crashes during live demonstrations.
    """
    print(f"🌍 Translating to {target_lang}...")
    
    try:
        gt = Translator()
        translated = gt.translate(text, dest=target_lang).text
        return translated
    except Exception as e:
        print(f"❌ Translation failed entirely: {e}")
        return text


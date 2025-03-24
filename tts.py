import os
from gtts import gTTS
from playsound import playsound
from googletrans import Translator

def translate_text(text, dest_lang='hi'):
    """
    Translates the given text into the specified language.
    """
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

def save_translated_text(text, filename='translated_hindi.txt'):
    """
    Saves the provided text into a file under the static/Text folder with UTF-8 encoding to preserve Hindi characters.
    """
    # Use the directory of the current file to build the path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    text_dir = os.path.join(base_dir, 'static', 'Text')
    os.makedirs(text_dir, exist_ok=True)
    file_path = os.path.join(text_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return file_path

def text_to_speech(text, lang='hi', filename='output.mp3'):
    """
    Converts text to speech using gTTS and saves it as an MP3 file.
    """
    tts = gTTS(text, lang=lang)
    tts.save(filename)
    return filename

def play_audio(filename='output.mp3'):
    """
    Plays the specified audio file.
    """
    playsound(filename)

if __name__ == "__main__":
    sample_text = "Hello, this is a test message."
    hindi_text = translate_text(sample_text, dest_lang='hi')
    print("Translated Text:", hindi_text)
    
    # Save the translated Hindi text in static/Text folder.
    saved_file = save_translated_text(hindi_text)
    print("Translated Hindi text saved to:", saved_file)
    
    audio_file = text_to_speech(hindi_text, lang='hi')
    play_audio(audio_file)

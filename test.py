##for testing gtt prnounciation


from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io


def speak_text_google(text):
    tts = gTTS(text=text, lang='fr', slow=False)
    # Convert to an in-memory file object
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    # Load the audio data into an AudioSegment
    audio = AudioSegment.from_file(fp, format="mp3")

    # Play the audio
    play(audio)


# Example usage
speak_text_google("Bonjour, comment ça va?")

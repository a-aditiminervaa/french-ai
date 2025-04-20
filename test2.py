import boto3
from pydub import AudioSegment
from pydub.playback import play
import io

def speak_text_polly(text):
    # Create a Polly client
    polly = boto3.client('polly')

    # Request speech synthesis
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Celine',  # Use a French voice like Celine or Mathieu
        LanguageCode='fr-FR'
    )

    # Read the audio stream
    audio_stream = response['AudioStream'].read()

    # Load the audio data into an AudioSegment
    audio = AudioSegment.from_file(io.BytesIO(audio_stream), format="mp3")

    # Play the audio
    play(audio)

# Example usage
speak_text_polly("Bonjour, comment ça va?")

import os
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from phonemizer import phonemize
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from Levenshtein import ratio
import sounddevice as sd
import soundfile as sf
import random
import time
import subprocess
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io
import csv


EspeakWrapper.set_library('C:\\Program Files\\eSpeak NG\\libespeak-ng.dll')

# Set environment variable for eSpeak NG data path
os.environ['ESPEAK_DATA_PATH'] = "C:\\Program Files\\eSpeak NG"

# Load the French-specific model and processor
model_name = "facebook/wav2vec2-large-xlsr-53-french"
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name).to(device)

def transcribe_audio(audio_path):
    # Load audio
    speech, rate = sf.read(audio_path)
    if rate != 16000:
        raise ValueError("The audio sample rate must be 16000 Hz.")

    # Ensure audio is a 1D array
    if len(speech.shape) > 1:
        speech = speech[:, 0]  # Use the first channel if stereo

    # Process the audio
    input_values = processor(speech, sampling_rate=rate, return_tensors="pt", padding="longest").input_values.to(device)
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    return transcription.lower()

def phonetic_comparison(reference_text, user_transcription):
    try:
        # Convert to phonemes using the espeak backend
        print("Converting reference text to phonemes...")
        reference_phonemes = phonemize(reference_text, language='fr-fr', backend='espeak', strip=True, njobs=1)
        print("Reference text phonemized successfully.")

        print("Converting user transcription to phonemes...")
        user_phonemes = phonemize(user_transcription, language='fr-fr', backend='espeak', strip=True, njobs=1)
        print("User transcription phonemized successfully.")

        # Compare phonemes
        similarity_score = ratio(reference_phonemes, user_phonemes)
        accuracy = similarity_score * 100
        print(f"Phonetic Accuracy: {accuracy:.2f}%")

        # Feedback
        if similarity_score > 0.8:
            print("Your pronunciation is good!")

        else:
            print("Your pronunciation needs improvement.")

        #compares the phonemes of the user and the refrence
        print(f"Reference Phonemes: {reference_phonemes}")
        print(f"User Phonemes: {user_phonemes}")

    except Exception as e:
        print(f"Error during phoneme conversion: {e}")

def record_audio(duration=3, fs=16000):
    print("Recording will start in 2 seconds...")
    time.sleep(2)
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until the recording is finished
    return audio.flatten()

def save_audio(audio, filename="user_audio.wav", fs=16000):
    sf.write(filename, audio, fs)

def speak_text(text):
    # Use gTTS for speech synthesis
    tts = gTTS(text=text, lang='fr', slow=False)
    # Convert to an in-memory file object
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    # Load the audio data into an AudioSegment
    audio = AudioSegment.from_file(fp, format="mp3")

    # Play the audio
    play(audio)

def get_words_from_csv(file_path):
    words = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.extend(row)  # Assuming each row contains a single word
    return words

# Example Usage
file_path = "frenchWordsDataset.csv"  # Update this path to your actual CSV file
french_words = get_words_from_csv(file_path)
reference_text = random.choice(french_words)

# Inform and pronounce the word for the user
print(f"Please say the following word: {reference_text}")
speak_text(reference_text)

# Record and save user's pronunciation
user_audio = record_audio()
save_audio(user_audio, "user_audio.wav")

# Transcribe and analyze
user_transcription = transcribe_audio("user_audio.wav")
print("You said:", user_transcription)
phonetic_comparison(reference_text, user_transcription)

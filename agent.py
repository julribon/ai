from pyexpat import model

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from piper import PiperVoice

from ai.agent import lms_agent
from ai.agent.ollama_agent import OllamaAgent


AGENT_NAME = "Alix"  # Mot-clé pour activer l'assistant 
BYE_KEYWORDS = ["au revoir", "à bientôt", "ce sera tout", "c'est tout", "merci"]  # Mots-clés pour terminer la conversation

# SPEECH-TO-TEXT
# Initialize the Whisper model for speech-to-text
SAMPLE_RATE = 16000
BLOCK_DURATION = 4  # secondes
whisper_model = WhisperModel("turbo", device="cpu", compute_type="int8")


# TEXTE-TO-SPEECH
# Load the Piper voice model
VOICE_PATH = "voice/fr_FR-upmc-medium.onnx"
voice = PiperVoice.load(VOICE_PATH)

# Initialize the Ollama's LLM
SYSTEM_PROMPT = (
    f"Tu es {AGENT_NAME}, une assistante vocal francophone. "
    "Sois concis, clair et naturel dans tes réponses."
    "Répond au maximum avec 3 phrases."
    "Répond avec des phrases, mais pas de code ni de formats spéciaux."
)
agent = OllamaAgent(system_prompt=SYSTEM_PROMPT) # model_name='qwen3.8:27b-mlx'


def record_audio(duration, sample_rate):
    # Record audio from the microphone
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    audio = audio.flatten()  # Flatten the array to 1D (audio[:, 0])
    return audio

def transcribe_audio(audio, model):
    segments, _ = model.transcribe(audio, language="fr", vad_filter=True)
    text = " ".join(s.text for s in segments).strip()
    return text

def listen():
    print("Listening...")
    audio = record_audio(BLOCK_DURATION, SAMPLE_RATE)
    text = transcribe_audio(audio, whisper_model)

    if text: 
        print(f"User: {text}") 

    return text


def speak(response):
    # Synthesize the response using the Piper voice model
    audio_chunks = []

    for chunk in voice.synthesize(response):

        # Convert the audio chunk to a NumPy array
        audio_chunk = np.frombuffer(
            chunk.audio_int16_bytes, 
            dtype=np.int16
        )
        audio_chunks.append(audio_chunk)

    audio = np.concatenate(audio_chunks)

    sd.play(audio, samplerate=chunk.sample_rate)
    sd.wait()


def main():
    print("Recording...")

    while True:
        text = listen()

        if AGENT_NAME.lower() in text.lower():
            print("Agent's name detected. Activating...")

            response = agent.ask(f"Bonjour {AGENT_NAME}!")
            speak(response)

            while not any(w in text.lower() for w in BYE_KEYWORDS):
                text = listen()

                # Speaks only if needed
                if text:
                    response = agent.ask(text)
                    speak(response)

            print("Goodbye keyword detected. Ending conversation...")

if __name__ == "__main__":
    main()

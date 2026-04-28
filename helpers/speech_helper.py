"""Helper functions for interoperating with Azure Speech service."""

import azure.cognitiveservices.speech as speechsdk
from config import SPEECH_KEY, SPEECH_REGION

def synthesize_speech(text: str) -> str:
    """Synthesize text to speech using Azure Speech Service."""
    try:
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        
        # Example using the default speaker
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        result = speech_synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}]".format(text))
            return "Success"
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
            return "Failed to synthesize speech."
    except Exception as e:
        print(f"Error in speech synthesis: {e}")
        return str(e)
    return "Error"

def recognize_speech() -> str:
    """Recognize speech from the default microphone (STT)."""
    try:
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        print("Listening for speech...")
        result = speech_recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
            return "No background speech matched."
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            return "Speech recognition canceled."
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return f"Error: {e}"
    return ""

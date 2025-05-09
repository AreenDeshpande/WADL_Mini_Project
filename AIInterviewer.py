import time
import numpy as np
import sounddevice as sd
import whisper
import pygame
from gtts import gTTS
from io import BytesIO
from openai import OpenAI

# Initialize NVIDIA's integration endpoint with your API key.
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your API key if needed.
)

# Candidate's skillset
candidate_skillset = """
Problem Solving: DSA, OOP, DBMS, OS
Languages: C++, Java, Python, JavaScript
AI and ML Domain: NLP, CV, OCR, GenAI
Web Development: HTML, CSS, JavaScript, React.js, Express, Flask, Django, Git version control, Github
Database: MySQL, SQLite, PostgreSQL, Firebase
"""

# System prompt (hidden) instructing the LLM to ask 5 questions and then provide a final summary.
system_prompt = f"""
You are an interviewer. Use the candidate's skillset provided below to ask exactly 5 interview questions.
Candidate's Skillset:
{candidate_skillset}

For each candidate response, evaluate it as correct or incorrect and keep track of the number of correct and incorrect answers.
After 5 questions, conclude by saying "Thank you for appearing for the interview" along with a summary including:
- Total number of correct answers,
- Total number of incorrect answers,
- Whether the candidate has cleared the interview (pass if at least 70% answers are correct).

Do not display any internal thoughts or system details in your output. Only ask the questions and provide the final summary.
"""

# Build the conversation history.
conversation = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": "Let's begin the interview. Here is your first question:"}
]

# Initialize pygame mixer for text-to-speech.
pygame.mixer.init()

# Load the Whisper model (using the "base" model as an example) for transcription.
print("Loading Whisper model for transcription...")
whisper_model = whisper.load_model("base")
print("Whisper model loaded.")

def record_audio(duration, fs=16000):
    """
    Record audio from the microphone for a given duration.
    Returns a 1D float32 numpy array normalized to [-1, 1].
    """
    print("Recording your answer...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished.
    print("Recording complete.")
    # Convert from int16 to float32 normalized in [-1, 1]
    audio = recording.astype(np.float32) / 32768.0
    return audio.flatten()

def transcribe_audio(audio, fs=16000):
    """
    Transcribe the provided audio (a numpy array) using the Whisper model.
    Returns the transcribed text.
    """
    print("Transcribing your answer...")
    result = whisper_model.transcribe(audio, language="en")
    return result["text"]

def speak(text):
    """
    Convert text to speech using gTTS and play it via pygame.
    """
    print("Speaking out:", text)
    tts = gTTS(text=text, lang='en')
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    pygame.mixer.music.load(audio_stream, 'mp3')
    pygame.mixer.music.play()
    # Wait until the audio finishes playing.
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def get_candidate_answer(duration=15, fs=16000):
    """
    Prompts the candidate to record an answer and returns the transcribed text.
    """
    input("\nPress Enter to start recording your answer (recording will last {} seconds)...".format(duration))
    audio = record_audio(duration, fs)
    transcription = transcribe_audio(audio, fs)
    print("You said:", transcription)
    return transcription

def main():
    num_questions = 5
    question_count = 0

    # Speak out the initial interview message.
    speak(conversation[-1]["content"])

    while question_count < num_questions:
        # Capture candidate's answer using voice.
        candidate_answer = get_candidate_answer(duration=15)
        if candidate_answer.strip().lower() == "exit":
            conversation.append({"role": "user", "content": candidate_answer})
            break

        # Append candidate's answer to conversation history.
        conversation.append({"role": "user", "content": candidate_answer})
        question_count += 1

        # Determine the prompt suffix based on the question count.
        if question_count < num_questions:
            prompt_suffix = "Please ask the next interview question based on the candidate's skillset."
        else:
            prompt_suffix = ("Please conclude the interview by saying 'Thank you for appearing for the interview' and "
                             "provide a performance summary including the total number of correct and incorrect answers, "
                             "and whether the candidate passed with at least 70% correct answers.")

        conversation_context = conversation + [{"role": "assistant", "content": prompt_suffix}]

        # Call the NVIDIA LLM endpoint to get the next interview prompt or final summary.
        completion = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=conversation_context,
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        assistant_reply = completion.choices[0].message.content
        print("\nInterviewer:", assistant_reply, "\n")
        # Convert the LLM's response to speech.
        speak(assistant_reply)
        conversation.append({"role": "assistant", "content": assistant_reply})

        # Break if the interview is concluded.
        if "Thank you for appearing for the interview" in assistant_reply:
            break

    print("Interview session ended.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterview session terminated by user.")

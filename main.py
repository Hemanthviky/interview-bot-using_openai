import os
import openai
import json
import wave
import pyaudio
from dotenv import load_dotenv
import keyboard
import requests
import io
from pydub import AudioSegment
from pydub.playback import play
import PyPDF2
from tkinter import Tk
from tkinter.filedialog import askopenfilename


load_dotenv()

# openai key and the org id which is present in the .env file
openai.api_key = os.getenv("OPEN_AI_KEY")
openai.organization = os.getenv("OPEN_AI_ORG")
elevenlabkey = os.getenv("ELEVENLAB_KEY")


# Function to capture audio in real time
def capture_audio(filename="output.wav"):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    frames = []  # Initialize array to store frames

    print("Press 's' to start recording, and 'e' to stop.")

    # Wait for 's' key to start recording
    keyboard.wait('s')
    print("Recording...")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    while True:
        if keyboard.is_pressed('e'):
            print("Stopping...")
            break
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PortAudio interface
    p.terminate()

    print("Finished recording.")

    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

    return filename


# Function to transcribe audio to text using OpenAI's Whisper model
def transcribe_audio(filename):
    with open(filename, "rb") as audio_file:
        transcription = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
        print(f"User: {transcription.text}")
        return transcription.text


# Function to get chat response from OpenAI's GPT-3.5-turbo
def get_chat_response(user_message, pdf_text, pdf_text_jd):
    messages = load_messages(pdf_text, pdf_text_jd)
    messages.append({"role": "user", "content": user_message})
    gpt_response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    chat_message_content = gpt_response.choices[0].message.content
    save_messages(user_message, chat_message_content)
    print(f"Diagonal_lab_bot: {chat_message_content}")
    return chat_message_content


# Function to load the initial messages/prompt for GPT-3
def load_messages(pdf_text, pdf_text_jd):
    messages = []
    file = 'database.json'
    
    if os.path.exists(file) and os.stat(file).st_size > 0:
        with open(file) as db_file:
            messages = json.load(db_file)
    else:
        messages.append(
            {"role": "system", "content": f""""You are Billy and interviewing the user for the job description {pdf_text_jd}.
            Start by asking the user for a self-introduction of the user as one single question.
            Then, ask 2 questions related to the projects the user has done from the resume.
            Here is the extracted text from the resume: {pdf_text}, Next, ask 2 questions related to the job description.
            If the user doesn't know the answer, then ask simplified and refined questions.
            Finally, provide the user with full interview feedback, highlighting areas for improvement.
            Conclude by saying you had a nice time interviewing them, and say goodbye, encouraging them to return with improvements.
            The conversation should be interactive and occasionally funny.
            The important point is to ask only 5 or 6 questions, and ask the questions one by one."""},
        )
    return messages


# Save user and GPT responses to a JSON file
def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages(pdf_text, pdf_text_jd)
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, 'w') as f:
        json.dump(messages, f)


# Extract text from the selected PDF (Resume)
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    # Extract text from each page
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    
    return text


# File dialog to select PDF file (Resume)
def PDF_TEXT():
    root = Tk()
    root.withdraw()
    
    pdf_file_path = askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not pdf_file_path:
        print("No file selected.")
    else:
        try:
            with open(pdf_file_path, 'rb') as pdf_file:
                extracted_text = extract_text_from_pdf(pdf_file)
                return extracted_text
        except Exception as e:
            print(f"An error occurred: {e}")


# Extract text from the selected PDF (Job Description)
def extract_text_from_pdf_JD(pdf_file_JD):
    pdf_reader = PyPDF2.PdfReader(pdf_file_JD)
    text = ""
    
    # Extract text from each page
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    
    return text


# File dialog to select PDF file (Job Description)
def PDF_TEXT_JD():
    root = Tk()
    root.withdraw()

    pdf_file_path = askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not pdf_file_path:
        print("No file selected.")
    else:
        try:
            with open(pdf_file_path, 'rb') as pdf_file:
                extracted_text = extract_text_from_pdf_JD(pdf_file)
                return extracted_text
        except Exception as e:
            print(f"An error occurred: {e}")


# Function to convert text to speech using OpenAI TTS
def text_to_speech(input_text):
    # Create the TTS request
    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    
    audio_data = io.BytesIO(response.content)
    audio_segment = AudioSegment.from_file(audio_data, format="mp3")
    
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(audio_segment.sample_width),
                    channels=audio_segment.channels,
                    rate=audio_segment.frame_rate,
                    output=True)

    for chunk in audio_segment[::1024]:  # Play in chunks
        stream.write(chunk._data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()


# Initialize the PDFs and start the conversation
pdf_text = PDF_TEXT()
pdf_text_jd = PDF_TEXT_JD()

if __name__ == "__main__":
    # Start the conversation with the bot asking the first question
    gpt_initial_response = get_chat_response("", pdf_text, pdf_text_jd)
    text_to_speech(gpt_initial_response)
    
    while True:
        audio_file = capture_audio()
        user_message = transcribe_audio(audio_file)
        
        if user_message.strip().lower() == "stop":
            print("Conversation ended by the user.")
            break
        
        gpt_response = get_chat_response(user_message, pdf_text, pdf_text_jd)
        text_to_speech(gpt_response)

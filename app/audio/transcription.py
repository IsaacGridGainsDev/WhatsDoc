import os
import tempfile
from pydub import AudioSegment
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with API key
# Using OpenAI SDK version 0.28.1 which doesn't have the proxies parameter issue
openai.api_key = api_key

# Do not create a client instance with OpenAI() constructor as it's not compatible with v0.28.1

def transcribe_audio(file_path, transcription_type="cleaned", proofreading=True):
    """
    Transcribe audio file using OpenAI's Whisper API
    
    Args:
        file_path (str): Path to the audio file
        transcription_type (str): 'verbatim' or 'cleaned'
        proofreading (bool): Whether to proofread the transcription
        
    Returns:
        str: Transcribed text
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    # Convert audio to supported format if needed
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # If file is not in a supported format, convert it
    if file_extension not in [".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"]:
        temp_file = convert_audio_format(file_path)
        file_path = temp_file.name
    
    # Transcribe audio using Whisper API
    try:
        with open(file_path, "rb") as audio_file:
            # Set transcription parameters based on type
            response_format = "verbose_json" if transcription_type == "verbatim" else "text"
            
            # Call Whisper API using OpenAI SDK v0.28.1
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format=response_format
            )
            
            # Process the response based on transcription type
            if transcription_type == "verbatim":
                # Extract segments with timestamps
                segments = response.segments
                transcription = format_segments_with_timestamps(segments)
            else:
                # Simple text response
                transcription = response
            
            # Apply proofreading if enabled
            if proofreading:
                transcription = proofread_transcription(transcription)
            
            return transcription
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

def convert_audio_format(file_path):
    """
    Convert audio to MP3 format for Whisper API compatibility
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        tempfile.NamedTemporaryFile: Temporary file with converted audio
    """
    try:
        # Load audio file using pydub
        audio = AudioSegment.from_file(file_path)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        
        # Export as MP3
        audio.export(temp_file.name, format="mp3")
        
        return temp_file
    except Exception as e:
        raise Exception(f"Audio conversion failed: {str(e)}")

def format_segments_with_timestamps(segments):
    """
    Format transcription segments with timestamps
    
    Args:
        segments (list): List of transcription segments
        
    Returns:
        str: Formatted transcription with timestamps
    """
    formatted_text = ""
    
    for segment in segments:
        start_time = format_time(segment.start)
        end_time = format_time(segment.end)
        text = segment.text.strip()
        
        formatted_text += f"[{start_time} - {end_time}] {text}\n\n"
    
    return formatted_text

def format_time(seconds):
    """
    Format time in seconds to MM:SS format
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted time string
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def proofread_transcription(text):
    """
    Proofread transcription using GPT-4
    
    Args:
        text (str): Transcription text
        
    Returns:
        str: Proofread transcription
    """
    try:
        # Call GPT-4 to proofread the transcription
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional transcription proofreader. Your task is to correct any errors in the transcription while preserving the original meaning. Fix spelling, grammar, and punctuation errors. Do not add or remove content."},
                {"role": "user", "content": f"Please proofread this transcription:\n\n{text}"}
            ]
        )
        
        # Extract the proofread text
        proofread_text = response.choices[0].message.content
        
        return proofread_text
    except Exception as e:
        # If proofreading fails, return the original text
        print(f"Proofreading failed: {str(e)}")
        return text
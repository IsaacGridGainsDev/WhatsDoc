# WhatsDoc Automator

WhatsDoc Automator is a Python application that converts WhatsApp voice notes and chats into professional documents. It streamlines the process of transcribing audio and structuring chat data into clean summaries, action lists, or formatted PDFs/DOCs.

## Features

- **Voice Note Transcription**: Upload and transcribe WhatsApp voice notes using OpenAI's Whisper API
- **Chat to Document Conversion**: Parse and structure WhatsApp messages
- **Document Templates**: Pre-loaded formats for different document types
- **Automation Panel**: Save presets and automate workflows
- **User Dashboard**: View, edit, and download past transcriptions

## Tech Stack

- **Frontend**: CustomTkinter (GUI)
- **Backend**: Python
- **Transcription API**: Whisper (OpenAI)
- **Summarization & Formatting**: GPT-4
- **Export**: python-docx, FPDF
- **Storage**: Local (MVP) / Firebase or SQLite for persistence

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in the `.env` file
4. Run the application:
   ```
   python main.py
   ```

## Project Structure

- `main.py`: Entry point for the application
- `app/`: Core application modules
  - `audio/`: Audio processing and transcription
  - `chat/`: Chat parsing and structuring
  - `document/`: Document generation and templates
  - `ui/`: User interface components
- `config/`: Configuration files
- `data/`: Local storage for user data
- `utils/`: Utility functions

## License

This project is licensed under the MIT License - see the LICENSE file for details.
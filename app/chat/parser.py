import os
import re
import datetime
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

def parse_chat(input_data, options):
    """
    Parse WhatsApp chat data and convert to structured format
    
    Args:
        input_data (dict): Input data with type and content
        options (dict): Processing options
        
    Returns:
        dict: Processed chat data with summary, action points, and full content
    """
    # Extract chat text based on input type
    if input_data["type"] == "text":
        chat_text = input_data["content"]
    elif input_data["type"] == "file":
        chat_text = read_chat_file(input_data["content"])
    elif input_data["type"] == "screenshots":
        chat_text = extract_text_from_screenshots(input_data["content"])
    else:
        raise ValueError(f"Unsupported input type: {input_data['type']}")
    
    # Parse chat messages
    messages = parse_whatsapp_messages(chat_text)
    
    # Structure the messages
    structured_chat = structure_messages(messages)
    
    # Generate results based on options
    result = {"full_content": format_structured_chat(structured_chat)}
    
    if options.get("summary", False):
        result["summary"] = generate_summary(structured_chat, options.get("template", "Meeting Summary"))
    
    if options.get("action_points", False):
        result["action_points"] = extract_action_points(structured_chat)
    
    return result

def read_chat_file(file_path):
    """
    Read WhatsApp chat export file
    
    Args:
        file_path (str): Path to the chat export file
        
    Returns:
        str: Chat text content
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        # Try with different encodings
        encodings = ["latin-1", "iso-8859-1", "windows-1252"]
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Could not decode the file with any of the attempted encodings")

def extract_text_from_screenshots(image_paths):
    """
    Extract text from WhatsApp chat screenshots using OCR
    
    Args:
        image_paths (list): List of paths to screenshot images
        
    Returns:
        str: Extracted text from all screenshots
    """
    # This would use an OCR library to extract text from images
    # For the MVP, we'll return a placeholder message
    return "[OCR functionality will be implemented in a future version. Please use text input for now.]"

def parse_whatsapp_messages(chat_text):
    """
    Parse WhatsApp chat text into individual messages
    
    Args:
        chat_text (str): Raw WhatsApp chat text
        
    Returns:
        list: List of message dictionaries with date, sender, and content
    """
    # Regular expression to match WhatsApp message format
    # Format: [date, time] sender: message
    pattern = r'\[?(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\]?\s+-?\s+([^:]+):\s+(.+)'
    
    messages = []
    current_message = None
    
    for line in chat_text.split('\n'):
        match = re.match(pattern, line)
        if match:
            # If we have a current message, add it to the list
            if current_message:
                messages.append(current_message)
            
            # Extract message components
            date_str, time_str, sender, content = match.groups()
            
            # Create new message
            current_message = {
                "date": date_str,
                "time": time_str,
                "sender": sender.strip(),
                "content": content.strip()
            }
        elif current_message:
            # Continuation of previous message
            current_message["content"] += "\n" + line.strip()
    
    # Add the last message
    if current_message:
        messages.append(current_message)
    
    return messages

def structure_messages(messages):
    """
    Structure messages by date and sender
    
    Args:
        messages (list): List of message dictionaries
        
    Returns:
        dict: Structured chat data
    """
    structured_chat = {}
    
    for message in messages:
        date = message["date"]
        sender = message["sender"]
        
        # Initialize date entry if not exists
        if date not in structured_chat:
            structured_chat[date] = {}
        
        # Initialize sender entry if not exists
        if sender not in structured_chat[date]:
            structured_chat[date][sender] = []
        
        # Add message to sender's list for this date
        structured_chat[date][sender].append({
            "time": message["time"],
            "content": message["content"]
        })
    
    return structured_chat

def format_structured_chat(structured_chat):
    """
    Format structured chat data as readable text
    
    Args:
        structured_chat (dict): Structured chat data
        
    Returns:
        str: Formatted chat text
    """
    formatted_text = ""
    
    for date in sorted(structured_chat.keys()):
        formatted_text += f"=== {date} ===\n\n"
        
        for sender in structured_chat[date]:
            for message in structured_chat[date][sender]:
                formatted_text += f"[{message['time']}] {sender}: {message['content']}\n"
            
            formatted_text += "\n"
        
        formatted_text += "\n"
    
    return formatted_text

def generate_summary(structured_chat, template_type):
    """
    Generate a summary of the chat using GPT-4
    
    Args:
        structured_chat (dict): Structured chat data
        template_type (str): Type of document template
        
    Returns:
        str: Generated summary
    """
    # Format chat for GPT input
    formatted_chat = format_structured_chat(structured_chat)
    
    # Limit input size
    if len(formatted_chat) > 12000:  # Approximate token limit
        formatted_chat = formatted_chat[:12000] + "\n[Chat truncated due to length...]\n"
    
    # Create system prompt based on template type
    system_prompt = get_template_prompt(template_type)
    
    try:
        # Call GPT-4 to generate summary
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please summarize this WhatsApp chat:\n\n{formatted_chat}"}
            ]
        )
        
        # Extract the summary
        summary = response.choices[0].message.content
        
        return summary
    except Exception as e:
        # If summarization fails, return error message
        print(f"Summarization failed: {str(e)}")
        return f"Error generating summary: {str(e)}"

def extract_action_points(structured_chat):
    """
    Extract action points from the chat using GPT-4
    
    Args:
        structured_chat (dict): Structured chat data
        
    Returns:
        str: Extracted action points
    """
    # Format chat for GPT input
    formatted_chat = format_structured_chat(structured_chat)
    
    # Limit input size
    if len(formatted_chat) > 12000:  # Approximate token limit
        formatted_chat = formatted_chat[:12000] + "\n[Chat truncated due to length...]\n"
    
    try:
        # Call GPT-4 to extract action points
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts action items, tasks, and commitments from WhatsApp conversations. For each action item, identify who is responsible, what the task is, and any deadlines mentioned. Format the output as a bulleted list with clear, concise points."},
                {"role": "user", "content": f"Please extract all action points from this WhatsApp chat:\n\n{formatted_chat}"}
            ]
        )
        
        # Extract the action points
        action_points = response.choices[0].message.content
        
        return action_points
    except Exception as e:
        # If extraction fails, return error message
        print(f"Action point extraction failed: {str(e)}")
        return f"Error extracting action points: {str(e)}"

def get_template_prompt(template_type):
    """
    Get system prompt based on template type
    
    Args:
        template_type (str): Type of document template
        
    Returns:
        str: System prompt for GPT
    """
    templates = {
        "Meeting Summary": "You are an assistant that summarizes meeting discussions from WhatsApp chats. Create a professional meeting summary with these sections: 1) Meeting Overview, 2) Key Discussion Points, 3) Decisions Made, and 4) Next Steps. Format the summary in a clear, professional style suitable for business documentation.",
        
        "Client Brief": "You are an assistant that creates client briefs from WhatsApp conversations. Summarize the client's requirements, preferences, timeline, budget, and any other relevant details. Format the output as a professional client brief document that could be shared with a team.",
        
        "Sales Report": "You are an assistant that generates sales reports from WhatsApp conversations. Extract information about sales activities, client interactions, opportunities, challenges, and results. Format the output as a professional sales report with sections for overview, key accounts, pipeline, and forecast.",
        
        "Real Estate Checklist": "You are an assistant that creates real estate checklists from WhatsApp conversations. Extract property details, client requirements, viewing notes, and follow-up items. Format the output as a structured checklist that a real estate agent could use to track the property transaction process."
    }
    
    return templates.get(template_type, templates["Meeting Summary"])
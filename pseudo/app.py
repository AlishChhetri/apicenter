"""
Main Flask application for Pseudo.
"""
import os
import shutil
import logging
import requests
from pathlib import Path
from flask import Flask, jsonify, request, send_file, render_template
from apicenter.apicenter import apicenter
from pseudo.media_handler import MediaHandler
from pseudo.chat_history import ChatHistory
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_credentials():
    """
    Set up the credentials path in the environment.
    Ensures credentials are available in the virtual environment.
    """
    # Get the virtual environment path
    venv_path = Path(os.environ.get("VIRTUAL_ENV", ""))
    if not venv_path:
        raise RuntimeError("Virtual environment not found")

    # Source credentials path (project root)
    source_credentials = Path(__file__).parent.parent / "credentials.json"
    if not source_credentials.exists():
        raise FileNotFoundError(
            "credentials.json not found in project root. Please create one using the template."
        )

    # Destination credentials path (virtual environment)
    dest_credentials = venv_path / "lib" / "python3.12" / "site-packages" / "credentials.json"
    
    # Copy credentials to virtual environment
    shutil.copy2(source_credentials, dest_credentials)
    
    # Set the environment variable
    os.environ["APICENTER_CREDENTIALS_PATH"] = str(dest_credentials)
    logger.info("Credentials set up successfully")

# Set up credentials before importing apicenter
setup_credentials()

app = Flask(__name__)
media_handler = MediaHandler()
chat_history = ChatHistory()

def detect_mode(input_text: str) -> str:
    """
    Detect the mode of the input (text, image, or audio).
    This is a simple implementation that can be enhanced with more sophisticated detection.
    """
    # Simple keyword-based detection
    if any(keyword in input_text.lower() for keyword in ["image", "picture", "photo", "draw", "generate image"]):
        return "image"
    elif any(keyword in input_text.lower() for keyword in ["speak", "voice", "audio", "sound"]):
        return "audio"
    return "text"

def download_image(url: str) -> bytes:
    """Download image from URL and return bytes."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
        raise

@app.route("/")
def index():
    """
    Serve the main application page.
    """
    return render_template('chat.html')

@app.route('/api/chats')
def get_chats():
    """Get all chat histories."""
    try:
        return jsonify(chat_history.get_all_chats())
    except Exception as e:
        logger.error(f"Error getting chats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chats/<chat_id>')
def get_chat(chat_id):
    """Get a specific chat's history."""
    try:
        chat = chat_history.get_chat_history(chat_id)
        if not chat:
            return jsonify({'error': 'Chat not found'}), 404
        return jsonify(chat)
    except Exception as e:
        logger.error(f"Error getting chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chats', methods=['POST'])
def create_chat():
    """Create a new chat session."""
    try:
        chat_id = chat_history.create_new_chat()
        return jsonify({"chat_id": chat_id})
    except Exception as e:
        logger.error(f"Error creating chat: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and generate responses."""
    try:
        data = request.get_json()
        message = data.get('message')
        chat_id = data.get('chat_id')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
            
        # Create new chat if none exists
        if not chat_id:
            chat_id = chat_history.create_new_chat()
            
        # Detect mode and get response
        mode = detect_mode(message)
        logger.info(f"Detected mode: {mode} for chat {chat_id}")
        
        # Get response based on mode
        if mode == "text":
            response = apicenter.text(
                provider="openai",
                model="gpt-4",
                prompt=message,
                temperature=0.7,
                max_tokens=500
            )
            output_type = "text"
            output_path = None
            
        elif mode == "image":
            try:
                response = apicenter.image(
                    provider="openai",
                    model="dall-e-3",
                    prompt=message,
                    size="1024x1024",
                    quality="standard",
                    style="vivid"
                )
                
                if isinstance(response, list):
                    image_url = response[0]  # Use first image if multiple returned
                else:
                    image_url = response
                    
                # Download the image
                image_bytes = download_image(image_url)
                
                # Save image and get path
                output_path = chat_history.save_output_file(chat_id, image_bytes, "png")
                output_type = "image"
                
            except Exception as e:
                logger.error(f"Error generating image: {e}")
                return jsonify({"error": "Failed to generate image"}), 500
                
        elif mode == "audio":
            try:
                # First, get a transcript of what will be said
                transcript = message.replace("speak", "").replace("voice", "").replace("audio", "").replace("sound", "").strip()
                if not transcript:
                    transcript = "No text provided for audio generation"
                
                # Generate the audio with minimal parameters
                audio_response = apicenter.audio(
                    provider="elevenlabs",
                    model="eleven_multilingual_v2",
                    prompt=transcript
                )
                
                if not isinstance(audio_response, bytes):
                    logger.error(f"Invalid audio response: {audio_response}")
                    return jsonify({"error": "Failed to generate audio"}), 500
                
                # Save audio and get path
                output_path = media_handler.save_audio(audio_response, transcript)
                if not output_path:
                    raise Exception("Failed to save audio file")
                
                output_type = "audio"
                response = transcript  # Use the transcript as the response text
                
            except Exception as e:
                logger.error(f"Error generating audio: {e}")
                return jsonify({"error": "Failed to generate audio"}), 500
                
        else:
            return jsonify({"error": f"Unsupported mode: {mode}"}), 400
        
        # Log the message with proper response
        chat_history.log_message(
            chat_id=chat_id,
            user_input=message,
            response=response,
            output_type=output_type,
            output_path=output_path
        )
        
        return jsonify({
            'chat_id': chat_id,
            'response': response,
            'output_type': output_type,
            'output_path': output_path,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/output/<path:filename>')
def serve_media(filename):
    """Serve media files from the output directory."""
    try:
        # Get the absolute path to the file
        file_path = Path(__file__).parent.parent / 'output' / filename
        if not file_path.exists():
            logger.error(f"Media file not found: {file_path}")
            return jsonify({"error": "File not found"}), 404
            
        # Determine the MIME type based on file extension
        mime_type = None
        if file_path.suffix.lower() == '.png':
            mime_type = 'image/png'
        elif file_path.suffix.lower() == '.mp3':
            mime_type = 'audio/mpeg'
            
        logger.info(f"Serving media file: {file_path}")
        return send_file(
            file_path,
            mimetype=mime_type,
            as_attachment=False
        )
    except Exception as e:
        logger.error(f"Error serving media file {filename}: {e}")
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    setup_credentials()
    app.run(debug=True) 
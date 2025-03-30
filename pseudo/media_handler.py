"""
Media handler for saving and serving generated media files.
"""
import os
from pathlib import Path
from typing import Optional, Union, List
from PIL import Image
import io
import requests
from flask import send_file
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MediaHandler:
    """Handles saving and serving of generated media files."""
    
    def __init__(self, base_dir: str = None):
        """
        Initialize the media handler.
        
        Args:
            base_dir: Base directory for saving media files (defaults to project root)
        """
        if base_dir is None:
            # Use project root directory
            base_dir = Path(__file__).parent.parent
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(exist_ok=True)
        
        # Create output directory
        self.output_dir = self.base_dir / 'output'
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different media types
        self.image_dir = self.output_dir / 'images'
        self.audio_dir = self.output_dir / 'audio'
        self.image_dir.mkdir(exist_ok=True)
        self.audio_dir.mkdir(exist_ok=True)
        
        logger.info(f"Media handler initialized with base directory: {self.base_dir}")
    
    def save_image(self, response: Union[str, bytes, List[str]], prompt: str) -> Optional[str]:
        """
        Save an image from a URL, bytes, or DALL-E response.
        
        Args:
            response: URL, bytes, or DALL-E response list
            prompt: The prompt used to generate the image
            
        Returns:
            Path to the saved image or None if there was an error
        """
        try:
            # Generate a filename from the prompt
            filename = f"{hash(prompt)}_{len(list(self.image_dir.glob('*')))}.png"
            filepath = self.image_dir / filename
            
            logger.info(f"Saving image to: {filepath}")
            
            # Handle different response types
            if isinstance(response, list):  # DALL-E response
                logger.info("Processing DALL-E response")
                if not response:
                    raise ValueError("Empty DALL-E response")
                # DALL-E returns a list with a URL
                url = response[0]
                img_response = requests.get(url)
                img_response.raise_for_status()
                img = Image.open(io.BytesIO(img_response.content))
            elif isinstance(response, str):  # URL from other providers
                logger.info(f"Downloading image from URL: {response}")
                img_response = requests.get(response)
                img_response.raise_for_status()
                img = Image.open(io.BytesIO(img_response.content))
            else:  # Bytes from Stability
                logger.info("Processing image from bytes")
                img = Image.open(io.BytesIO(response))
            
            # Save the image
            img.save(filepath, "PNG")
            logger.info(f"Image saved successfully to: {filepath}")
            return str(filepath)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading image: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            return None
    
    def save_audio(self, audio_data: bytes, prompt: str) -> Optional[str]:
        """
        Save audio data to a file.
        
        Args:
            audio_data: The audio data in bytes
            prompt: The prompt used to generate the audio
            
        Returns:
            Path to the saved audio file or None if there was an error
        """
        try:
            # Generate a filename from the prompt
            filename = f"{hash(prompt)}_{len(list(self.audio_dir.glob('*')))}.mp3"
            filepath = self.audio_dir / filename
            
            logger.info(f"Saving audio to: {filepath}")
            
            # Save the audio file
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            logger.info(f"Audio saved successfully to: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving audio: {str(e)}")
            return None
    
    def serve_media(self, filepath: str):
        """
        Serve a media file through Flask.
        
        Args:
            filepath: Path to the media file
            
        Returns:
            Flask response with the media file
        """
        try:
            filepath = Path(filepath).resolve()
            if not filepath.exists():
                logger.error(f"File not found: {filepath}")
                return None
            return send_file(filepath)
        except Exception as e:
            logger.error(f"Error serving media file: {str(e)}")
            return None 
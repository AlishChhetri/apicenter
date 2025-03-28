"""
Advanced usage examples for APICenter.

This example demonstrates:
1. Error handling
2. Provider-specific parameters
3. Rate limiting
4. Response handling
5. Advanced features
"""

import os
from typing import Optional
from apicenter import apicenter
from PIL import Image
import io

class APICenterAdvanced:
    """Advanced usage examples for APICenter."""
    
    @staticmethod
    def handle_text_generation(
        provider: str,
        model: str,
        prompt: str,
        **kwargs
    ) -> Optional[str]:
        """
        Safely generate text with error handling.
        
        Args:
            provider: The AI provider to use
            model: The model to use
            prompt: The input prompt
            **kwargs: Additional parameters for the provider
            
        Returns:
            The generated text or None if there was an error
        """
        try:
            response = apicenter.text(
                provider=provider,
                model=model,
                prompt=prompt,
                **kwargs
            )
            return response
        except Exception as e:
            print(f"Error generating text with {provider}: {str(e)}")
            return None
    
    @staticmethod
    def handle_image_generation(
        provider: str,
        model: str,
        prompt: str,
        save_path: Optional[str] = None,
        **kwargs
    ) -> Optional[Image.Image]:
        """
        Safely generate and optionally save an image.
        
        Args:
            provider: The AI provider to use
            model: The model to use
            prompt: The input prompt
            save_path: Optional path to save the image
            **kwargs: Additional parameters for the provider
            
        Returns:
            The generated image as PIL Image or None if there was an error
        """
        try:
            response = apicenter.image(
                provider=provider,
                model=model,
                prompt=prompt,
                **kwargs
            )
            
            # Handle different response types
            if isinstance(response, str):  # URL from DALL-E
                import requests
                img_response = requests.get(response)
                img = Image.open(io.BytesIO(img_response.content))
            else:  # Bytes from Stability
                img = Image.open(io.BytesIO(response))
            
            # Save if path provided
            if save_path:
                img.save(save_path)
                print(f"Image saved to {save_path}")
            
            return img
        except Exception as e:
            print(f"Error generating image with {provider}: {str(e)}")
            return None
    
    @staticmethod
    def handle_audio_generation(
        provider: str,
        model: str,
        prompt: str,
        save_path: Optional[str] = None,
        **kwargs
    ) -> Optional[bytes]:
        """
        Safely generate and optionally save audio.
        
        Args:
            provider: The AI provider to use
            model: The model to use
            prompt: The input prompt
            save_path: Optional path to save the audio
            **kwargs: Additional parameters for the provider
            
        Returns:
            The generated audio as bytes or None if there was an error
        """
        try:
            audio = apicenter.audio(
                provider=provider,
                model=model,
                prompt=prompt,
                **kwargs
            )
            
            # Save if path provided
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(audio)
                print(f"Audio saved to {save_path}")
            
            return audio
        except Exception as e:
            print(f"Error generating audio with {provider}: {str(e)}")
            return None

def main():
    """Run advanced examples."""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Text generation with error handling
    print("\nGenerating text with error handling...")
    text = APICenterAdvanced.handle_text_generation(
        provider="anthropic",
        model="claude-3-sonnet-20240229",
        prompt="Write a short story about a robot learning to paint.",
        temperature=0.7,
        max_tokens=500
    )
    if text:
        print("Generated text:", text)
    
    # Image generation with saving
    print("\nGenerating image with saving...")
    img = APICenterAdvanced.handle_image_generation(
        provider="openai",
        model="dall-e-3",
        prompt="A beautiful sunset over mountains, digital art style",
        save_path="output/generated_image.png",
        size="1024x1024",
        quality="standard",
        style="vivid"
    )
    if img:
        print("Image generated successfully!")
    
    # Audio generation with saving
    print("\nGenerating audio with saving...")
    audio = APICenterAdvanced.handle_audio_generation(
        provider="elevenlabs",
        model="eleven_multilingual_v2",
        prompt="Hello! This is a test of text to speech.",
        save_path="output/generated_audio.mp3",
        voice_id="21m00Tcm4TlvDq8ikWAM",
        stability=0.5,
        similarity_boost=0.75
    )
    if audio:
        print("Audio generated successfully!")

if __name__ == "__main__":
    main() 
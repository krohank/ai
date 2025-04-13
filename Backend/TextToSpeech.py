import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")  # Corrected from .Get to .get

# Asynchronous function to convert text to audio
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

# Function to manage TTS playback
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to speech
            asyncio.run(TextToAudioFile(Text))
            
            # Initialize and play audio
            pygame.mixer.init()
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)
            
            return True
        
        except Exception as e:
            print(f"Error in TTS: {e}")
        
        finally:
            try:
                func(False)  # Signal completion
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in cleanup: {e}")

# Function to handle long text segmentation
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    responses = [
        "Shall I continue?",
        "Would you like me to go on?",
        "Should I proceed with the rest?",
        "Do you want to hear more?"
    ]
    
    if len(Data) > 4 and len(Text) >= 250:
        # Play first two sentences + random response
        partial_text = " ".join(Text.split(".")[0:2]) + ". " + random.choice(responses)
        TTS(partial_text, func)
    else:
        TTS(Text, func)

# Main execution
if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))  # Added missing parenthesis

"""Module providing functionality to create a mp3 file via the tiktok tts api."""
# author: GiorDior aka Giorgio
# date: 12.06.2023
# topic: TikTok-Voice-TTS
# version: 1.0
# credits: https://github.com/oscie57/tiktok-voice

import threading
import base64
import requests
from tts.tiktok.voices import voices

ENDPOINTS = [
    'https://tiktok-tts.weilnet.workers.dev/api/generation',
    "https://tiktoktts.com/api/tiktok-tts"
]
# in one conversion, the text can have a maximum length of 300 characters
TEXT_BYTE_LIMIT = 300

def split_string(string: str, chunk_size: int) -> list[str]:
    """Function create a list by splitting a string, every element has n chars"""
    words = string.split()
    result = []
    current_chunk = ''
    for word in words:
        # Check if adding the word exceeds the chunk size
        if len(current_chunk) + len(word) + 1 <= chunk_size:
            current_chunk += ' ' + word
        else:
            # Append the current chunk if not empty
            if current_chunk:
                result.append(current_chunk.strip())
            current_chunk = word
    # Append the last chunk if not empty
    if current_chunk:
        result.append(current_chunk.strip())
    return result

def get_api_response(current_endpoint: int) -> requests.Response:
    """Function checking if the website that provides the service is available"""
    url = f'{ENDPOINTS[current_endpoint].split("/a", maxsplit=1)[0]}'
    response = requests.get(url, timeout=60)
    return response

def save_audio_file(base64_data: str, filename: str = "output.mp3") -> None:
    """Function saving the audio file"""
    audio_bytes = base64.b64decode(base64_data)
    with open(filename, "wb") as file:
        file.write(audio_bytes)

def generate_audio(text: str, voice: str, current_endpoint: int) -> bytes:
    """Function send POST request to get the audio data"""
    url = f'{ENDPOINTS[current_endpoint]}'
    headers = {'Content-Type': 'application/json'}
    data = {'text': text, 'voice': voice}
    response = requests.post(url, headers=headers, json=data, timeout=60)
    return response.content

# pylint: disable=too-many-branches
def tts(text: str, voice: str = "none", filename: str = "output.mp3") -> None:
    """Function creates an text to speech audio file"""

    # checking if the website is available
    current_endpoint = 0

    if get_api_response(current_endpoint).status_code == 200:
        print("Service available!")
    else:
        current_endpoint = (current_endpoint + 1) % 2
        if get_api_response(current_endpoint).status_code == 200:
            print("Service available!")
        else:
            print("Service not available and probably temporarily rate limited, try again later...")
            return

    # checking if arguments are valid
    if voice == "none":
        print("No voice has been selected")
        return

    if voice not in voices:
        print("Voice does not exist")
        return

    if len(text) == 0:
        print("Insert a valid text")
        return

    # creating the audio file
    try:
        if len(text) < TEXT_BYTE_LIMIT:
            audio = generate_audio((text), voice, current_endpoint)
            if current_endpoint == 0:
                audio_base64_data = str(audio).split('"')[5]
            else:
                audio_base64_data = str(audio).split('"')[3].split(",")[1]

            if audio_base64_data == "error":
                print("This voice is unavailable right now")
                return

        else:
            # Split longer text into smaller parts
            text_parts = split_string(text, 299)
            audio_base64_data = [None] * len(text_parts)

            # pylint: disable=inconsistent-return-statements
            def generate_audio_thread(text_part, index):
                """Function Define a thread function to generate audio for each text part"""

                audio = generate_audio(text_part, voice, current_endpoint)
                if current_endpoint == 0:
                    base64_data = str(audio).split('"')[5]
                else:
                    base64_data = str(audio).split('"')[3].split(",")[1]

                if audio_base64_data == "error":
                    print("This voice is unavailable right now")
                    return "error"

                # pylint: disable=unsupported-assignment-operation
                audio_base64_data[index] = base64_data

            threads = []
            for index, text_part in enumerate(text_parts):
                # Create and start a new thread for each text part
                thread = threading.Thread(target=generate_audio_thread, args=(text_part, index))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            # Concatenate the base64 data in the correct order
            audio_base64_data = "".join(audio_base64_data)

        save_audio_file(audio_base64_data, filename)
        print(f"Audio file saved successfully as '{filename}'")

    # pylint: disable=broad-exception-caught
    except Exception as e:
        print("Error occurred while generating audio:", str(e))

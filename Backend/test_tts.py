from app.services.tts_service import GnaniTTS


tts = GnaniTTS()

text = """
My name is mayank singh. its a dummy project by me. 
"""

audio = tts.generate(text)

with open("test_output.wav", "wb") as file:
    file.write(audio)

print(
    f"Audio generated successfully: {len(audio)} bytes"
)
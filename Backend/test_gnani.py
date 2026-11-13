import requests

from app.config import GNANI_API_KEY


URL = "https://api.vachana.ai/api/v1/tts/inference"


def test_tts(text: str):
    payload = {
        "text": text,
        "model": "timbre-v2.5",
        "voice": "Kaveri",
        "language": "en-IN",
        "speed": 1.0,
        "audio_config": {
            "sample_rate": 48000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav",
        },
    }

    response = requests.post(
        URL,
        headers={
            "X-API-Key-ID": GNANI_API_KEY,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )

    print(
        f"Characters: {len(text)} | "
        f"Words: {len(text.split())} | "
        f"Status: {response.status_code}"
    )

    if response.ok:
        print("SUCCESS")
    else:
        print(response.text)


tests = [
    "Hello, this is a short test.",
    " ".join(["Hello"] * 100),
    " ".join(["Hello"] * 200),
    " ".join(["Hello"] * 300),
    " ".join(["Hello"] * 400),
    " ".join(["Hello"] * 500),
]


for text in tests:
    test_tts(text)
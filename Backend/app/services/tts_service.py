import io
import time
import wave
import requests

from app.config import GNANI_API_KEY


class GnaniTTS:

    def __init__(self):
        self.url = (
            "https://api.vachana.ai/api/v1/tts/inference"
        )

    def _generate_chunk(self, text: str) -> bytes:

        payload = {
            "text": text,
            "model": "timbre-v2.5",
            "voice": "Kaveri",
            "language": "en-IN",
            "speed": 0.9,
            "audio_config": {
                "sample_rate": 48000,
                "num_channels": 1,
                "sample_width": 2,
                "encoding": "linear_pcm",
                "container": "wav",
            },
        }

        response = requests.post(
            self.url,
            headers={
                "X-API-Key-ID": GNANI_API_KEY,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=120,
        )

        if not response.ok:
            raise Exception(
                f"Gnani TTS failed "
                f"({response.status_code}): "
                f"{response.text}"
            )

        return response.content

    def _split_text(
        self,
        text: str,
        max_chars: int = 1000,
    ) -> list[str]:

        sentences = []

        current = ""

        # Split primarily on sentence boundaries
        for sentence in text.replace(
            "?", "?|"
        ).replace(
            "!", "!|"
        ).replace(
            ".", ".|"
        ).split("|"):

            sentence = sentence.strip()

            if not sentence:
                continue

            candidate = (
                f"{current} {sentence}"
                if current
                else sentence
            )

            if len(candidate) <= max_chars:
                current = candidate

            else:
                if current:
                    sentences.append(current)

                # Handle an individual sentence
                # larger than max_chars.
                if len(sentence) > max_chars:

                    words = sentence.split()

                    chunk = ""

                    for word in words:

                        candidate = (
                            f"{chunk} {word}"
                            if chunk
                            else word
                        )

                        if len(candidate) <= max_chars:
                            chunk = candidate
                        else:
                            if chunk:
                                sentences.append(chunk)

                            chunk = word

                    if chunk:
                        current = chunk
                    else:
                        current = ""

                else:
                    current = sentence

        if current:
            sentences.append(current)

        return sentences

    def _combine_wav(
        self,
        audio_chunks: list[bytes],
    ) -> bytes:

        output = io.BytesIO()

        with wave.open(output, "wb") as output_wav:

            first = True

            for audio in audio_chunks:

                with wave.open(
                    io.BytesIO(audio),
                    "rb",
                ) as input_wav:

                    if first:

                        output_wav.setnchannels(
                            input_wav.getnchannels()
                        )

                        output_wav.setsampwidth(
                            input_wav.getsampwidth()
                        )

                        output_wav.setframerate(
                            input_wav.getframerate()
                        )

                        first = False

                    frames = input_wav.readframes(
                        input_wav.getnframes()
                    )

                    output_wav.writeframes(
                        frames
                    )

        return output.getvalue()

    def generate(self, text: str) -> bytes:

        chunks = self._split_text(
            text,
            max_chars=1000,
        )

        print(
            f"Sending text to Gnani TTS: "
            f"{len(text)} characters / "
            f"{len(text.split())} words"
        )

        print(
            f"Split into {len(chunks)} TTS chunks."
        )

        audio_chunks = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            print(
                f"TTS chunk {index}/{len(chunks)}: "
                f"{len(chunk)} characters"
            )

            audio = self._generate_chunk(
                chunk
            )

            audio_chunks.append(audio)

            # Avoid hammering the API
            if index < len(chunks):
                time.sleep(0.5)

        final_audio = self._combine_wav(
            audio_chunks
        )

        print(
            "Gnani TTS generation successful."
        )

        return final_audio
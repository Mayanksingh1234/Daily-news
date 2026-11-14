import os
import requests

from dotenv import load_dotenv

load_dotenv()


class EmailService:
    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY")
        self.from_email = os.getenv(
            "RESEND_FROM_EMAIL",
            "onboarding@resend.dev",
        )

        if not self.api_key:
            raise RuntimeError(
                "RESEND_API_KEY is not configured"
            )

        self.url = "https://api.resend.com/emails"

    def send_episode_email(
        self,
        to_email: str,
        title: str,
        audio_url: str,
    ):
        payload = {
            "from": self.from_email,
            "to": [to_email],
            "subject": f"Your Daily Podcast: {title}",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">

                    <h2>Your Daily Podcast is Ready</h2>

                    <p>
                        Your scheduled research briefing
                        <strong>{title}</strong>
                        has been generated successfully.
                    </p>

                    <p>
                        You can listen to your episode using
                        the button below.
                    </p>

                    <p style="margin: 30px 0;">
                        <a
                            href="{audio_url}"
                            style="
                                display: inline-block;
                                padding: 12px 20px;
                                background: #111827;
                                color: white;
                                text-decoration: none;
                                border-radius: 6px;
                            "
                        >
                            Listen to Podcast
                        </a>
                    </p>

                    <p style="color: #6b7280; font-size: 13px;">
                        This email was automatically generated
                        by your Daily Podcast Agent.
                    </p>

                </div>
            """,
        }

        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )

        if not response.ok:
            raise Exception(
                f"Resend email failed "
                f"({response.status_code}): "
                f"{response.text}"
            )

        print(
            f"[EMAIL] Episode email sent to {to_email}"
        )

        return response.json()
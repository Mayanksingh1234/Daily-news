import os
from dotenv import load_dotenv

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv(
    "SUPABASE_SECRET_KEY"
)

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GNANI_API_KEY = os.getenv(
    "GNANI_API_KEY"
)

SUPABASE_AUDIO_BUCKET = os.getenv(
    "SUPABASE_AUDIO_BUCKET",
    "episodes"
)

RESEND_API_KEY = os.getenv(
    "RESEND_API_KEY"
)

RESEND_FROM_EMAIL = os.getenv(
    "RESEND_FROM_EMAIL",
    "onboarding@resend.dev"
)


if not SUPABASE_URL:
    raise RuntimeError(
        "SUPABASE_URL is not configured"
    )

if not SUPABASE_SECRET_KEY:
    raise RuntimeError(
        "SUPABASE_SECRET_KEY is not configured"
    )

if not TAVILY_API_KEY:
    raise RuntimeError(
        "TAVILY_API_KEY is not configured"
    )

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured"
    )

if not GNANI_API_KEY:
    raise RuntimeError(
        "GNANI_API_KEY is not configured"
    )

if not RESEND_API_KEY:
    raise RuntimeError(
        "RESEND_API_KEY is not configured"
    )
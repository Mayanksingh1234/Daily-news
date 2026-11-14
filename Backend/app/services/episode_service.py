from app.agents.research_agent import ResearchAgent
from app.database import supabase
from app.services.script_generator import ScriptGenerator
from app.services.tts_service import GnaniTTS
from app.config import SUPABASE_AUDIO_BUCKET
from app.services.email_service import EmailService


research_agent = ResearchAgent()
script_generator = ScriptGenerator()
tts_service = GnaniTTS()
email_service = EmailService()


def get_user_email(user_id: str) -> str:
    """
    Retrieve the user's email from Supabase Auth.
    """

    response = (
        supabase.auth.admin.get_user_by_id(
            user_id
        )
    )

    if not response or not response.user:
        raise Exception(
            "Unable to retrieve user information"
        )

    email = response.user.email

    if not email:
        raise Exception(
            "User does not have an email address"
        )

    return email


def generate_episode(
    episode_id: str,
    briefing_id: str,
    topic: str,
):
    try:

        # -----------------------------------------
        # 1. Get episode/user information
        # -----------------------------------------

        episode_response = (
            supabase
            .table("episodes")
            .select("user_id, title")
            .eq("id", episode_id)
            .single()
            .execute()
        )

        episode = episode_response.data

        if not episode:
            raise Exception(
                "Episode not found"
            )

        user_id = episode["user_id"]

        title = (
            episode.get("title")
            or topic
        )

        # -----------------------------------------
        # 2. Get user email
        # -----------------------------------------

        user_email = get_user_email(
            user_id
        )

        print(
            f"[EMAIL] User email: {user_email}"
        )

        # -----------------------------------------
        # 3. Mark episode as researching
        # -----------------------------------------

        supabase.table("episodes").update({
            "status": "researching"
        }).eq(
            "id",
            episode_id
        ).execute()

        # -----------------------------------------
        # 4. Research topic
        # -----------------------------------------

        sources = research_agent.research(
            topic
        )

        if not sources:
            raise Exception(
                "No research sources found"
            )

        # -----------------------------------------
        # 5. Save sources
        # -----------------------------------------

        source_rows = []

        for source in sources:
            source_rows.append({
                "episode_id": episode_id,
                "title": source.get("title"),
                "url": source.get("url"),
                "published_at": source.get(
                    "published_at"
                ),
            })

        if source_rows:
            (
                supabase
                .table("sources")
                .insert(source_rows)
                .execute()
            )

        # -----------------------------------------
        # 6. Generate podcast script
        # -----------------------------------------

        supabase.table("episodes").update({
            "status": "generating_script"
        }).eq(
            "id",
            episode_id
        ).execute()

        script = script_generator.generate(
            topic=topic,
            sources=sources,
        )

        print(
            f"Script length: "
            f"{len(script)} characters"
        )

        print(
            f"Script words: "
            f"{len(script.split())} words"
        )

        if not script:
            raise Exception(
                "Failed to generate podcast script"
            )

        # -----------------------------------------
        # 7. Save script
        # -----------------------------------------

        supabase.table("episodes").update({
            "script": script
        }).eq(
            "id",
            episode_id
        ).execute()

        # -----------------------------------------
        # 8. Generate audio
        # -----------------------------------------

        supabase.table("episodes").update({
            "status": "generating_audio"
        }).eq(
            "id",
            episode_id
        ).execute()

        audio_bytes = tts_service.generate(
            script
        )

        if not audio_bytes:
            raise Exception(
                "Gnani TTS returned empty audio"
            )

        # -----------------------------------------
        # 9. Upload audio
        # -----------------------------------------

        storage_path = (
            f"{episode_id}.wav"
        )

        (
            supabase
            .storage
            .from_(SUPABASE_AUDIO_BUCKET)
            .upload(
                storage_path,
                audio_bytes,
                {
                    "content-type": "audio/wav",
                    "upsert": "true",
                },
            )
        )

        # -----------------------------------------
        # 10. Get public audio URL
        # -----------------------------------------

        audio_url = (
            supabase
            .storage
            .from_(SUPABASE_AUDIO_BUCKET)
            .get_public_url(
                storage_path
            )
        )

        # -----------------------------------------
        # 11. Mark episode ready
        # -----------------------------------------

        (
            supabase
            .table("episodes")
            .update({
                "audio_url": audio_url,
                "status": "ready",
            })
            .eq(
                "id",
                episode_id
            )
            .execute()
        )

        print(
            f"[EPISODE] Episode ready: "
            f"{episode_id}"
        )

        # -----------------------------------------
        # 12. Send email
        # -----------------------------------------

        try:

            email_service.send_episode_email(
                to_email=user_email,
                title=title,
                audio_url=audio_url,
            )

            print(
                f"[EMAIL] Email sent successfully "
                f"to {user_email}"
            )

        except Exception as email_error:

            # Email failure should NOT make
            # the successfully generated
            # episode fail.

            print(
                f"[EMAIL ERROR] "
                f"{email_error}"
            )

        # -----------------------------------------
        # 13. Return completed episode
        # -----------------------------------------

        return {
            "episode_id": episode_id,
            "status": "ready",
            "script": script,
            "audio_url": audio_url,
            "sources": sources,
        }

    except Exception as error:

        supabase.table("episodes").update({
            "status": "failed",
            "error_message": str(error),
        }).eq(
            "id",
            episode_id
        ).execute()

        raise
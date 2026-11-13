from app.agents.research_agent import ResearchAgent
from app.database import supabase
from app.services.script_generator import ScriptGenerator
from app.services.tts_service import GnaniTTS
from app.config import SUPABASE_AUDIO_BUCKET


research_agent = ResearchAgent()
script_generator = ScriptGenerator()
tts_service = GnaniTTS()


def generate_episode(
    episode_id: str,
    briefing_id: str,
    topic: str,
):
    try:
        # -----------------------------------------
        # 1. Mark episode as researching
        # -----------------------------------------

        supabase.table("episodes").update({
            "status": "researching"
        }).eq(
            "id",
            episode_id
        ).execute()

        # -----------------------------------------
        # 2. Research topic
        # -----------------------------------------

        sources = research_agent.research(topic)

        if not sources:
            raise Exception(
                "No research sources found"
            )

        # -----------------------------------------
        # 3. Save sources
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
            supabase.table("sources").insert(
                source_rows
            ).execute()

        # -----------------------------------------
        # 4. Generate podcast script
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
        print(f"Script length: {len(script)} characters")
        print(f"Script words: {len(script.split())} words")

        if not script:
            raise Exception(
                "Failed to generate podcast script"
            )

        # -----------------------------------------
        # 5. Save script
        # -----------------------------------------

        supabase.table("episodes").update({
            "script": script
        }).eq(
            "id",
            episode_id
        ).execute()

        # -----------------------------------------
        # 6. Generate audio
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
        # 7. Upload audio to Supabase Storage
        # -----------------------------------------

        storage_path = (
            f"{episode_id}.wav"
        )

        supabase.storage.from_(
            SUPABASE_AUDIO_BUCKET
        ).upload(
            storage_path,
            audio_bytes,
            {
                "content-type": "audio/wav",
                "upsert": "true",
            },
        )

        # -----------------------------------------
        # 8. Get public audio URL
        # -----------------------------------------

        audio_url = (
            supabase.storage
            .from_(SUPABASE_AUDIO_BUCKET)
            .get_public_url(storage_path)
        )

        # -----------------------------------------
        # 9. Mark episode ready
        # -----------------------------------------

        supabase.table("episodes").update({
            "audio_url": audio_url,
            "status": "ready",
        }).eq(
            "id",
            episode_id
        ).execute()

        # -----------------------------------------
        # 10. Return completed episode
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
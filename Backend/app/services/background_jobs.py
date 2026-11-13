from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.database import supabase
from app.services.episode_service import generate_episode


def process_episode(
    episode_id: str,
    briefing_id: str,
    topic: str,
):
    """
    Runs the complete episode generation pipeline
    in the background.
    """

    print(
        f"[BACKGROUND] Starting episode generation: {episode_id}"
    )

    try:
        result = generate_episode(
            episode_id=episode_id,
            briefing_id=briefing_id,
            topic=topic,
        )

        print(
            f"[BACKGROUND] Episode completed: {episode_id}"
        )

        return result

    except Exception as error:
        print(
            f"[BACKGROUND] Episode failed: "
            f"{episode_id} - {error}"
        )


def create_episode_for_briefing(
    briefing: dict,
):
    """
    Creates an episode for a scheduled briefing
    and starts the generation pipeline.
    """

    briefing_id = briefing["id"]
    user_id = briefing["user_id"]
    topic = briefing["topic"]

    scheduled_time = briefing["scheduled_time"]
    timezone_name = briefing.get(
        "timezone",
        "Asia/Kolkata",
    )

    tz = ZoneInfo(timezone_name)

    now = datetime.now(tz)

    scheduled_for = now.replace(
        hour=int(scheduled_time[:2]),
        minute=int(scheduled_time[3:5]),
        second=0,
        microsecond=0,
    )

    # Prevent duplicate generation for the same
    # briefing on the same scheduled occurrence.
    existing = (
        supabase
        .table("episodes")
        .select("id")
        .eq("briefing_id", briefing_id)
        .eq(
            "scheduled_for",
            scheduled_for.astimezone(
                timezone.utc
            ).isoformat(),
        )
        .limit(1)
        .execute()
    )

    if existing.data:
        print(
            f"[SCHEDULER] Episode already exists "
            f"for briefing {briefing_id}"
        )
        return

    episode_data = {
        "briefing_id": briefing_id,
        "user_id": user_id,
        "title": topic,
        "status": "pending",
        "scheduled_for": scheduled_for.astimezone(
            timezone.utc
        ).isoformat(),
    }

    response = (
        supabase
        .table("episodes")
        .insert(episode_data)
        .execute()
    )

    if not response.data:
        print(
            f"[SCHEDULER] Failed to create episode "
            f"for briefing {briefing_id}"
        )
        return

    episode = response.data[0]

    print(
        f"[SCHEDULER] Created episode "
        f"{episode['id']}"
    )

    process_episode(
        episode_id=episode["id"],
        briefing_id=briefing_id,
        topic=topic,
    )


def check_scheduled_briefings():
    """
    Runs every minute.

    Finds active briefings whose scheduled time
    matches the current local time.
    """

    print("[SCHEDULER] Checking scheduled briefings...")

    response = (
        supabase
        .table("briefings")
        .select("*")
        .eq("active", True)
        .execute()
    )

    briefings = response.data or []

    for briefing in briefings:

        try:
            timezone_name = briefing.get(
                "timezone",
                "Asia/Kolkata",
            )

            tz = ZoneInfo(timezone_name)

            now = datetime.now(tz)

            scheduled_time = briefing["scheduled_time"]

            scheduled_hour = int(
                scheduled_time[:2]
            )

            scheduled_minute = int(
                scheduled_time[3:5]
            )

            if (
                now.hour == scheduled_hour
                and now.minute == scheduled_minute
            ):
                print(
                    f"[SCHEDULER] Time matched for "
                    f"briefing: {briefing['id']}"
                )

                create_episode_for_briefing(
                    briefing
                )

        except Exception as error:
            print(
                f"[SCHEDULER] Error processing "
                f"briefing {briefing['id']}: {error}"
            )
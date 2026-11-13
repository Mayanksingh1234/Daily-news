from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
)

from app.auth.dependencies import get_current_user
from app.database import supabase
from app.services.background_jobs import process_episode


router = APIRouter(
    prefix="/briefings",
    tags=["Episodes"],
)


@router.post(
    "/{briefing_id}/generate",
    status_code=status.HTTP_202_ACCEPTED,
)
async def generate_episode(
    briefing_id: UUID,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
):

    briefing_response = (
        supabase
        .table("briefings")
        .select("*")
        .eq("id", str(briefing_id))
        .eq("user_id", user["id"])
        .single()
        .execute()
    )

    briefing = briefing_response.data

    if not briefing:
        raise HTTPException(
            status_code=404,
            detail="Briefing not found",
        )

    episode_data = {
        "briefing_id": str(briefing_id),
        "user_id": user["id"],
        "title": briefing["topic"],
        "status": "pending",
    }

    response = (
        supabase
        .table("episodes")
        .insert(episode_data)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create episode",
        )

    episode = response.data[0]

    background_tasks.add_task(
        process_episode,
        episode_id=episode["id"],
        briefing_id=str(briefing_id),
        topic=briefing["topic"],
    )

    return {
        "status": "accepted",
        "message": "Episode generation started.",
        "episode": episode,
    }

@router.get("/{briefing_id}/episodes")
async def get_episodes(
    briefing_id: UUID,
    user=Depends(get_current_user),
):
    # Verify that the briefing belongs to the user
    briefing_response = (
        supabase
        .table("briefings")
        .select("id")
        .eq("id", str(briefing_id))
        .eq("user_id", user["id"])
        .single()
        .execute()
    )

    if not briefing_response.data:
        raise HTTPException(
            status_code=404,
            detail="Briefing not found",
        )

    response = (
        supabase
        .table("episodes")
        .select(
            "id, briefing_id, title, script, audio_url, "
            "status, error_message, generated_at, created_at"
        )
        .eq("briefing_id", str(briefing_id))
        .eq("user_id", user["id"])
        .order("created_at", desc=True)
        .execute()
    )

    return response.data
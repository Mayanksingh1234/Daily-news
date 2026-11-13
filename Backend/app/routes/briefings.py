from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.database import supabase
from app.schemas.briefing import BriefingCreate, BriefingUpdate


router = APIRouter(
    prefix="/briefings",
    tags=["Briefings"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_briefing(
    briefing: BriefingCreate,
    user=Depends(get_current_user),
):
    data = {
        "user_id": user["id"],
        "topic": briefing.topic,
        "scheduled_time": briefing.scheduled_time.isoformat(),
        "timezone": briefing.timezone,
        "active": True,
    }

    response = (
        supabase
        .table("briefings")
        .insert(data)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create briefing",
        )

    return response.data[0]


@router.get("")
async def get_briefings(
    user=Depends(get_current_user),
):
    response = (
        supabase
        .table("briefings")
        .select("*")
        .eq("user_id", user["id"])
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


@router.patch("/{briefing_id}")
async def update_briefing(
    briefing_id: UUID,
    briefing: BriefingUpdate,
    user=Depends(get_current_user),
):
    update_data = briefing.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if "scheduled_time" in update_data:
        update_data["scheduled_time"] = (
            update_data["scheduled_time"].isoformat()
        )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update",
        )

    response = (
        supabase
        .table("briefings")
        .update(update_data)
        .eq("id", str(briefing_id))
        .eq("user_id", user["id"])
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Briefing not found",
        )

    return response.data[0]


@router.delete("/{briefing_id}")
async def delete_briefing(
    briefing_id: UUID,
    user=Depends(get_current_user),
):
    response = (
        supabase
        .table("briefings")
        .delete()
        .eq("id", str(briefing_id))
        .eq("user_id", user["id"])
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Briefing not found",
        )

    return {
        "status": "success",
        "message": "Briefing deleted",
    }
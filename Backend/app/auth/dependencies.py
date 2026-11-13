from fastapi import Header, HTTPException

from app.database import supabase


async def get_current_user(
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
        )

    token = authorization.split(" ", 1)[1]

    try:
        response = supabase.auth.get_user(token)

        user = response.user

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token",
            )

        return {
            "id": user.id,
            "email": user.email,
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

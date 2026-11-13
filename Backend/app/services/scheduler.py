from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.background_jobs import (
    check_scheduled_briefings,
)


scheduler = AsyncIOScheduler()


def start_scheduler():

    scheduler.add_job(
        check_scheduled_briefings,
        "interval",
        minutes=1,
        id="briefing_scheduler",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()

    print(
        "[SCHEDULER] Daily briefing scheduler started."
    )


def stop_scheduler():

    scheduler.shutdown(
        wait=False
    )

    print(
        "[SCHEDULER] Scheduler stopped."
    )
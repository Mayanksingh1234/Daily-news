from app.services.email_service import EmailService

def test_send_episode_email():
    email_service = EmailService()

    to_email = "singhmayank2702@gmail.com"
    title = "Test Episode"
    audio_url = "https://example.com/audio.mp3"
    email_service.send_episode_email(to_email, title, audio_url)

test_send_episode_email()

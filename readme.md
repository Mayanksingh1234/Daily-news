# Daily Podcast Agent

An AI-powered platform that turns a user's research topic into a daily podcast.

A user can create a briefing such as:

> "Startup funding announced in the last 24 hours"

and choose a time, for example 8:00 AM.

At the scheduled time, the system researches the topic, generates a short podcast script, converts it into audio, stores the episode, and sends the user an email with a link to listen.

## Features

- User authentication with Supabase
- Create and manage daily research briefings
- Set a custom daily time and timezone
- Automated background scheduling
- Web research using Tavily
- AI-generated podcast scripts using Google Gemini
- Text-to-speech using Gnani AI
- Audio storage using Supabase Storage
- Episode history and transcripts
- Email notifications using Resend
- User-specific data and episodes
- Duplicate protection for scheduled episodes

## How It Works

```text
User creates a briefing
        ↓
Scheduled time is reached
        ↓
Background scheduler detects the briefing
        ↓
Tavily researches the topic
        ↓
Gemini creates a 5-minute podcast script
        ↓
Gnani AI converts the script into audio
        ↓
Audio is stored in Supabase
        ↓
Episode is marked as ready
        ↓
User receives an email
        ↓
User listens from the dashboard
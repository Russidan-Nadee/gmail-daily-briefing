# Email & Calendar Assistant Skill

## Description
This skill reads Gmail emails, ranks them by importance, summarizes each email into bullet points, and creates Google Calendar events if an email contains a meeting or interview that is not already on the calendar.

## Capabilities
- Read emails (read-only)
- Rank emails by importance
- Summarize emails into bullet points
- Detect meeting/interview emails
- Create Google Calendar events (only when not already added)

## Scripts
- `python scripts/fetch_emails.py` — Fetch emails from the last 24 hours and print full content
- `python scripts/create_event.py --title "..." --date "YYYY-MM-DD" --time "HH:MM" [--duration 60]` — Create a Google Calendar event

## Input
- User request (e.g., "Summarize today's important emails")

## Output to User
For each email (sorted by importance, most important first):
```
#1
From: <sender>
Subject: <subject>
- bullet point summary
- bullet point summary
[📅 Calendar event created: <title> on <date> at <time>]  ← only if applicable
```

## Behavior
1. Run `fetch_emails.py` to get emails from the last 24 hours
2. Read and analyze all emails
3. Rank emails by importance internally (1 = most important) — do not show ranking logic to user
4. Summarize each email into bullet points
5. If a meeting or interview is detected in an email:
   - Check if the event already exists on Google Calendar (e.g., from a Google Calendar invite)
   - If the event does NOT exist yet, run `create_event.py` to create it
   - If the event already exists, skip — do not create a duplicate

## Notes
- Gmail and Google Calendar API required
- Can be triggered by user request or external scheduler (e.g., cron job)
- Date must be in `YYYY-MM-DD` format, time in `HH:MM` format when calling `create_event.py`
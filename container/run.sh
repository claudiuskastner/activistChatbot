#!/bin/bash

exec /app/.venv/bin/scheduleNotification &
exec /app/.venv/bin/scrapeEvents &
exec /app/.venv/bin/activistChatbot

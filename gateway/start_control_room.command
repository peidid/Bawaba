#!/bin/zsh
# Double-click to open the LIVE Bawaba control room (any of the 120 patients, real model calls).
# Close this Terminal window (or press Ctrl+C) to stop the server.
cd "$(dirname "$0")"
URL="http://127.0.0.1:8341/"

if lsof -iTCP:8341 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Control room server is already running."
else
  echo "Starting the control room server..."
  .env311/bin/python server.py &
  for i in {1..40}; do
    curl -s -o /dev/null "$URL" && break
    sleep 0.5
  done
fi

open "$URL"
echo ""
echo "Bawaba control room: $URL"
echo "  Live run:  pick a patient, then 'Send to AI tool'"
echo "  Demo run:  already selected on the right, press '▶ Play recording'"
echo "Leave this window open while presenting. Close it or press Ctrl+C to stop."
wait

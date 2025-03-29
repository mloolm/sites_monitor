#!/bin/bash
#Fake request from Telegram for debugging
# (insert the correct URL, for this, debug it in main.py - @app.post("/telegram/webhook/{webhook_hash}")).
WEBHOOK_URL="http://localhost:8000/telegram/webhook/be0cd23cc966550b9cdb34dc31e2e1b69fece2b8df4f29178aef4d42a22ac45d"

PAYLOAD='{
  "update_id": 123456789,
  "message": {
    "message_id": 1,
    "from": {
      "id": 6425916377,
      "is_bot": false,
      "first_name": "John",
      "last_name": "Doe",
      "username": "johndoe",
      "language_code": "en"
    },
    "chat": {
      "id": 6425916377,
      "first_name": "John",
      "last_name": "Doe",
      "username": "johndoe",
      "type": "private"
    },
    "date": 1698765432,
    "text": "/auth nmznno"
  }
}'

curl -X POST "$WEBHOOK_URL" \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD"
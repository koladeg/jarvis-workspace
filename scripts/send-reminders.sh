#!/bin/bash

# Bank document reminder
curl -X POST https://api.telegram.org/bot$(echo $TELEGRAM_BOT_TOKEN | cut -d: -f1):$(echo $TELEGRAM_BOT_TOKEN | cut -d: -f2)/sendMessage \
  -d chat_id="-5249388197" \
  -d text="🏦 **Bank Document Reminder**
  
Everyone needs to fill the bank document. Please complete and submit today.
  
⏰ Next reminder in 6 hours." 2>/dev/null


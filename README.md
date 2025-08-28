# File Store Bot (Koyeb + MongoDB)

Features
- Permanent deep links for uploads: users receive a shareable URL like `https://t.me/<bot>?start=dl_<code>`.  
- First 3 videos are free; on the 4th and beyond, an adjustable shortlink verification flow triggers; admin can reset verification.  
- Force-subscribe to channels, user count, broadcast to all users, and a manual premium unlock via UPI/GPay.

Environment Variables
- BOT_TOKEN, BASE_URL, WEBHOOK_SECRET  
- MONGO_URL, DB_NAME  
- OWNER_ID, ADMINS (space-separated IDs)  
- FORCE_SUB_CHANNELS (comma-separated -100 IDs)  
- FREE_VIDEO_LIMIT (default 3), VERIFY_EXPIRE (default 86400)  
- SHORTLINK_PROVIDERS JSON, e.g.:  
  `[{"name":"arolinks","type":"adlinkfly","api_url":"https://arolinks.com/api","api_key":"YOUR_AROLINKS_API_KEY"}]`  
- PREMIUM_UPI_ID (default sivaramanc49@okaxis), PREMIUM_QR_URL (default https://envs.sh/in5.jpg)

Local Dev
- `pip install -r requirements.txt`  
- Export env vars above.  
- `python app.py` then open `/setup` once to register the webhook.

Deploy to Koyeb
1. Push this repo to GitHub.  
2. Create a Koyeb Web Service -> GitHub -> select repo -> Use Dockerfile builder -> Deploy.  
3. After Healthy, set BASE_URL to the service URL (e.g., `https://yourapp-org.koyeb.app`).  
4. Visit `https://yourapp-org.koyeb.app/setup` once to register the webhook.

Admin Commands
- `/resetverify <user_id>`  
- `/users`  
- `/broadcast` (send by replying to a message)  
- `/setpremium <user_id> <on|off>`  
- `/premium` (UPI/GPay info for users)

Usage
- Send any document/video to get a permanent deep link.  
- Anyone with the deep link can fetch the file; after 3 videos per user, verification is required unless premium is active.

Notes
- For private channels in force-subscribe, add the bot as a member to check membership.  
- AroLinks uses AdLinkFly API; ensure your API key is valid in SHORTLINK_PROVIDERS.  

# 😎 MemeMailer™: Weekly Meme Chaos via GitHub Actions

Bring humor, confusion, and a tiny bit of emotional instability to your manager’s inbox—all powered by Reddit, Python, and GitHub Actions. MemeMailer™ is a scheduled prank engine that sends curated programming memes, sarcastic quotes, and ambiguous Walken signatures every Monday at 6:45 PM IST.

> “I got a fever... and the only prescription is vague HTML signatures.”

---

## What It Does

- 🚀 Fetches top memes from multiple tech subreddits (weighted for fairness)
- 💬 Scrapes a random programming quote from the wild web
- 🖼️ Formats it all into a beautiful HTML newsletter
- 📤 Emails it to a list of ~unsuspecting~ recipients
- 🔔 Adds a cryptic cowbell signature for emotional disturbance

---

## Powered By

- [x] `praw` for Reddit access  
- [x] `beautifulsoup4` + `requests` for quote scraping  
- [x] `smtplib` + GitHub Secrets Vault for secure email delivery  
- [x] GitHub Actions for cloud-based scheduling  
- [x] Python 3.11 (but works on most modern versions)

---

## How to Deploy Your Own

1. **Fork this repo**
2. Add secrets under `Settings > Secrets and Variables > Actions`:
   - `SENDER_EMAIL`
   - `SENDER_PASSWORD` (App Password recommended)
   - `RECIPIENT_EMAIL` (comma-separated list)
   - `SMTP_SERVER` (e.g. `smtp.gmail.com`)
   - `SMTP_PORT` (usually `465`)
   - `CLIENT_ID` & `CLIENT_SECRET` for Reddit API
3. Customize `JHop_MemeMailer.py` if needed
4. Done—your memes will now deliver weekly with zero manual involvement

💡 Manual test? Use the **Actions** tab and hit “Run Workflow”


## 😈 Disclaimer

This project is meant for educational and humorous purposes only. Use responsibly. Or irresponsibly, but document it for the rest of us.

To unsubscribe from MemeMailer™, forward the email to `/dev/null` and whisper your wishes into the void.

---

## 📬 Want More?

Ideas for future upgrades:
- 🔁 Meme rotation (no repeats)
- 🧪 Click tracking for Walken links
- 📈 Logging + analytics dashboard
- 🤖 Reply-to-meme autoresponder

import praw
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import requests
import os

# Reddit credentials from GitHub Secrets
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="JHop_MemeMailer"
)

# Subreddit weightings to normalize popularity
sub_weights = {
    "ProgrammerHumor": 25,
    "devhumor": 4,
    "SoftwareGore": 6,
    "techsupportgore": 6,
    "SysadminHumor": 4,
    "linuxmasterrace": 5,
    "webdev": 8,
    "BadUIBattles": 4
}

def adjusted_score(post, weights):
    sub_name = post.subreddit.display_name
    weight = weights.get(sub_name, 1)
    return post.score / (weight ** 1.2)

def fetch_memes(limit_total=10, min_score=50, per_sub_limit=5):
    all_memes = []
    for sub in sub_weights:
        print(f"🔍 Fetching from r/{sub}...")
        try:
            posts = reddit.subreddit(sub).top(time_filter="week", limit=per_sub_limit * 2)
            filtered = [
                {
                    "title": f"[r/{sub}] {post.title}",
                    "url": post.url,
                    "score": post.score,
                    "adjusted_score": adjusted_score(post, sub_weights)
                }
                for post in posts
                if post.score >= min_score and (
                    any(ext in post.url for ext in ['.jpg', '.jpeg', '.png', '.webp']) or
                    "i.redd.it" in post.url or "imgur.com" in post.url
                )
            ]
            filtered.sort(key=lambda x: x["adjusted_score"], reverse=True)
            all_memes.extend(filtered[:3])
        except Exception as e:
            print(f"Failed to fetch from r/{sub}: {e}")
    all_memes.sort(key=lambda x: x["adjusted_score"], reverse=True)
    return all_memes[:limit_total]

def fetch_quote():
    try:
        url = "https://codeforgeek.com/programming-quotes-that-are-funny-too/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        candidates = [
            tag.get_text(strip=True)
            for tag in soup.find_all(["li", "p"])
            if 40 < len(tag.get_text(strip=True)) < 180
        ]
        quotes = list(set(candidates))
        return random.choice(quotes) if quotes else "“// TODO: Insert meaningful quote once caffeine kicks in.”"
    except Exception as e:
        print(f"Couldn't fetch quote: {e}")
        return "“// TODO: Insert meaningful quote once caffeine kicks in.”"

def send_email(memes):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    recipient_emails = os.getenv("RECIPIENT_EMAIL", "").split(",")

    quote = fetch_quote()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = 'Traitor "Chinese Cowboy" San 😂'
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipient_emails)

    html_body = """
    <html>
    <body style="font-family:Arial, sans-serif; background-color:#f9f9f9; padding:20px;">
        <h2 style="color:#2b2b2b;">👨‍💻 Weekly Meme Digest</h2>
        <p>Here's your dose of programming nonsense, delivered fresh from the wilds of Reddit by your <b>LEAST</b> favorite dev:</p>
        <hr>
    """

    for i, meme in enumerate(memes):
        badge = "<span style='color:gold; font-weight:bold;'>🏆 Top Meme of the Week</span><br>" if i == 0 else ""
        html_body += f"""
        <div style="margin-bottom:25px;">
            {badge}
            <h3 style="color:#333;">{meme['title']} <span style="font-size:14px; color:#777;">👍 {meme['score']} upvotes</span></h3>
            <img src="{meme['url']}" alt="{meme['title']}" style="max-width:100%; border:1px solid #ddd; box-shadow:2px 2px 10px rgba(0,0,0,0.1);"/>
        </div>
        """

    html_body += f"""
    <hr>
    <h3 style="color:#2b2b2b;">🧠 Quote of the Week</h3>
    <blockquote style="font-style:italic; color:#555; padding-left:10px; border-left:4px solid #ccc;">
        “{quote}”
    </blockquote>
    <br>
    <hr>
    <p style="font-size:14px; color:#444;">
      Yours in chaos,<br>
      The MemeMailer™<br>
      <i>P.S. I got a fever...</i><br>
      <a href="https://www.youtube.com/shorts/ihFlchpS36Y" target="_blank"
         style="color:#d35400; font-weight:bold;" title="You know what it is.">
         Click here for the prescription 🔔
      </a>
    </p>
    <hr>
    <p style="font-size:12px; color:#777;">
        This newsletter is powered by JHop MemeMailer™<br>
        To unsubscribe, forward this email to the void and whisper your wishes into /dev/null.
    </p>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
        print("Meme newsletter sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Entry point for GitHub Actions
if __name__ == "__main__":
    memes = fetch_memes()
    if memes:
        send_email(memes)
    else:
        print("No memes fetched. Try again later or check Reddit API access.")
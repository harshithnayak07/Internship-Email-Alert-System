# Internship Email Alert System

I kept missing internship emails because they got buried in my inbox. So I built this — it checks my Gmail for anything internship or recruitment related and sends me a Telegram alert on my phone. Costs nothing, runs on GitHub Actions, and my laptop can stay off.

## How It Works

```
Gmail  -->  Gmail API  -->  Python checks if it's relevant  -->  Sends alert to Telegram
```

GitHub Actions runs this every 2 hours automatically.

## What You'll Need

- A Google Cloud project with Gmail API enabled
- A Telegram bot (takes 2 minutes to create)
- A GitHub repo to run it on schedule

## Setup Guide

### Step 1: Google Cloud + Gmail API

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create a new project (name it whatever you want)
3. Search for "Gmail API" and enable it
4. Go to **Credentials** > **Create Credentials** > **OAuth 2.0 Client ID**
5. Choose **Desktop app** as the type
6. Download the JSON file — this is your `credentials.json`

### Step 2: Get Your Token (First Time Only)

1. Put `credentials.json` in the project root folder
2. Run this in terminal:
   ```
   pip install -r requirements.txt
   python -m app.worker
   ```
3. A browser window pops up — sign in with your Google account and allow access
4. A `token.json` file gets saved automatically
5. You can delete `credentials.json` after this (the token is enough going forward)

### Step 3: Create a Telegram Bot

1. Open Telegram, search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`, pick a name, done — you get a bot token
3. Send any message to your new bot
4. Open this URL in browser (replace `YOUR_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
5. Look for `"chat":{"id":` — that number is your chat ID

### Step 4: Run Locally

1. Copy the example env file:
   ```
   cp .env.example .env
   ```
2. Open `.env` and fill in your values
3. Run:
   ```
   python -m app.worker
   ```
4. You should get a Telegram alert if you have any internship emails from today

### Step 5: Push to GitHub

```
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 6: Add GitHub Secrets

Go to your repo on GitHub > **Settings** > **Secrets and variables** > **Actions** > **New repository secret**

Add these four:

| Secret | What to put |
|--------|-------------|
| `GMAIL_CREDENTIALS_JSON` | Full contents of your `credentials.json` |
| `GMAIL_TOKEN_JSON` | Full contents of `token.json` |
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Your chat ID from step 3 |

### Step 7: Enable the Workflow

1. Go to **Actions** tab in your repo
2. Click "I understand my workflows, go ahead and enable them"
3. The monitor runs every 2 hours automatically
4. You can also trigger it manually from the Actions tab

## What It Detects

The system looks at subject lines and email content to figure out what's what:

- **Selected / Offer** — you got in!
- **Shortlisted / Next Round** — moving forward
- **Interview** — interview scheduled
- **Assessment / Coding Test** — test to take
- **Internship Opportunity** — new opening
- **General Recruitment** — general hiring email
- **Rejected / Negative** — filtered out, no alert sent

Rejection emails are detected and skipped so you don't get false alarms.

## Project Files

```
app/
  gmail/          - OAuth login, fetches emails from Gmail API
  processor/      - figures out what each email is about
  notifications/  - sends Telegram messages
  database/       - keeps track of what's already been alerted
  config.py       - reads your env variables
  worker.py       - ties everything together, this is what runs
tests/            - pytest tests
.github/workflows/monitor.yml  - the GitHub Actions schedule
```

## Things to Know

- This is **not real-time**. GitHub Actions checks every ~2 hours. You might get an alert a bit after the email arrives.
- Classification is keyword-based. It works well for standard recruitment emails but might miss weirdly worded ones.
- The state database (`state.db`) only stores message IDs and classifications — no email content is kept.
- All your secrets stay local or in GitHub Secrets. Nothing gets committed to the repo.

## Running Tests

```
python -m pytest tests/ -v
```

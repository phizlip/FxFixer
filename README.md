# FxFixer Discord Bot

A Discord bot that automatically converts Twitter/X links to fxtwitter.com for better embeds and removes tracking parameters.

## Features

- Converts `twitter.com` and `x.com` links to `fxtwitter.com`
- Removes tracking parameters from URLs
- Preserves original sender's avatar and name via webhooks
- Original sender can delete the rewritten message with ❌ reaction

## Setup

1. **Create a `.env` file** with your Discord bot token:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

2. **Run with Docker Compose**:
   ```bash
   docker compose up -d
   ```
   
   **To stop the bot**:
   ```bash
   docker compose down
   ```

## Bot Permissions Required

- Read Messages
- Send Messages
- Manage Messages (to delete original messages)
- Manage Webhooks (to create webhooks for user impersonation)
- Add Reactions (to delete embed messages)

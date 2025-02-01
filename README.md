[Click here to watch the Paradox Reels demo video](https://cdn.discordapp.com/attachments/1138824814270890024/1331628295762219038/Paradox_Reels.mp4?ex=679f7dfe&is=679e2c7e&hm=6771143d6cbe58426b77b724eb499abc20d1f2f76726ae32242b2e22d6d19219&)

# Discord Reels Bot

A **Discord bot** that provides a temporary “Reels” feature—users can upload images that remain active for 24 hours. Other users can view and like these images; the bot automatically removes them (and their associated likes) after expiration.

---

## Table of Contents

1. [Features](#features)  
2. [System Requirements](#system-requirements)  
3. [Installation](#installation)  
4. [Folder Structure](#folder-structure)  
5. [Usage](#usage)  
   - [Commands Overview](#commands-overview)  
   - [Example Workflow](#example-workflow)  
6. [Database Details](#database-details)  
7. [Bot Configuration](#bot-configuration)  
8. [Customization](#customization)  
9. [Known Issues & Limitations](#known-issues--limitations)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

## Features

- **Create Reels**: Users can upload a single image (PNG/JPG) that is publicly viewable.  
- **Temporary Storage**: Each Reel remains active for 24 hours. After that, the bot removes both the Reel and its associated likes.  
- **View Reels**: A simple “slideshow” interface (ephemeral to the viewer) that automatically navigates to the next Reel after 15 seconds of inactivity.  
- **User Likes**: Each user can like any Reel exactly once.  
- **Automated Cleanup**: A scheduled task runs every 10 minutes to remove expired Reels from the database.  
- **Slash Commands**: All functionality is accessed via Discord slash commands (e.g., `/reels create`, `/reels view`).  

---

## System Requirements

- **Python** 3.8+  
- **discord.py** 2.0+  
- **aiosqlite** (for asynchronous SQLite operations)  
- Optional: **python-dotenv** for loading bot tokens from a `.env` file  

---

## Installation

1. **Clone the Repository** (or download the folder):
   ```bash
   git clone https://github.com/your-username/discord-reels-bot.git
   ```
2. **Change Directory** to the project folder:
   ```bash
   cd discord-reels-bot
   ```
3. **(Recommended) Create & Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate       # On macOS/Linux
   venv\Scripts\activate          # On Windows
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Set Up Your Bot Token**:
   - Option A: **Hardcode** in `main.py`:  
     ```python
     bot.run("YOUR_BOT_TOKEN")
     ```
   - Option B: **Use `.env`** (with [python-dotenv](https://pypi.org/project/python-dotenv/)):  
     ```env
     DISCORD_BOT_TOKEN=YourDiscordBotTokenHere
     ```
     and then in `main.py`:
     ```python
     import os
     from dotenv import load_dotenv

     load_dotenv()
     token = os.getenv("DISCORD_BOT_TOKEN")
     bot.run(token)
     ```

---

## Folder Structure

Below is an **example** folder layout you might have. You can rename or reorganize as desired.

```
discord_reels_bot/
├── cogs/
│   └── reels.py         # Cog for the Reels feature
├── data/
│   └── database.db      # SQLite database file (auto-created if not found)
├── main.py              # Main bot file
├── requirements.txt     # Python dependencies
├── .gitignore           # Files/folders to ignore in Git
└── README.md            # This documentation
```

- **`cogs/`**: Contains all Cog (modular feature) files.  
- **`data/`**: Stores the SQLite database or other persistent data.  
- **`main.py`**: The entry point for running your bot.  
- **`.gitignore`**: Typical patterns to avoid committing unwanted files (`__pycache__`, `venv`, etc.).  

---

## Usage

After completing [Installation](#installation):

```bash
python main.py
```
Invite the bot to your server using an **OAuth2** link from your [Discord Developer Portal](https://discord.com/developers/applications).

### Commands Overview

- **`/reels create`**  
  Upload a new Reel by attaching a PNG or JPG.  
  - Each user can only have one active Reel at a time.  
  - Ephemeral confirmation message.

- **`/reels view`**  
  View a slideshow (ephemeral) of all available Reels.  
  - **Previous** (`◀️`), **Next** (`▶️`), **Like** (`❤️`).

- **`/reels terms`**  
  Shows usage terms or rules in an ephemeral message.

### Example Workflow

1. **User A** runs `/reels create` and uploads an image.  
2. The bot saves the Reel in the database, valid for 24 hours.  
3. **User B** runs `/reels view` to browse Reels, then likes User A’s reel.  
4. After 24 hours, the cleanup task deletes expired Reels and their associated likes.

---

## Database Details

- Uses **SQLite** (file stored as `database.db` in `data/` by default).  
- **Tables**:  
  - `reels`: Stores each Reel (`id`, `user_id`, `image_url`, `datetime`, `likes`).  
  - `reel_likes`: Tracks likes (`user_id`, `image_url`) for each reel.  
  - (Optional) Additional tables, such as `duty`, can be created for extra features.

**Data Retention**:  
A background task runs every 10 minutes (`@tasks.loop(minutes=10)`) to remove Reels older than 24 hours (`86400` seconds).

---

## Bot Configuration

- **Command Prefix**: If you still use prefix-based commands, it might be `'!'`; slash commands are handled via `app_commands`.  
- **Discord Intents**: `discord.Intents.all()`, which you must also enable in the [Discord Developer Portal](https://discord.com/developers/applications).  
- **Reconnecting**: `bot.run(token, reconnect=True)` ensures the bot attempts to reconnect if it’s disconnected.

---

## Customization

1. **Folder Names**: If you rename `cogs/` or `data/`, update references in your code.  
2. **Language/Texts**: All embed messages and strings can be adjusted in `reels.py` (e.g., from English to another language).  
3. **Cleanup Interval**: The 10-minute loop can be changed to 5 minutes, 1 hour, etc.  
4. **Expiration Time**: Currently 24 hours (`86400` seconds). Update if you want a different lifespan.  
5. **Idle Timer**: The slideshow auto-advances after 15 seconds of inactivity. Change in `ReelsView.idle_logic()` if desired.

---

## Known Issues & Limitations

- **One Reel Per User**: By default, each user can only upload one active reel. Remove that check if you want multiple reels per user.  
- **Static Images Only**: The bot rejects GIFs (`image/gif`). Extend the `ALLOWED_IMAGE_TYPES` check if needed.  
- **Ephemeral View**: By default, `/reels view` is ephemeral, so only the user who called it sees the Reels. Remove `ephemeral=True` if you want a public channel embed.  
- **Administrator Permissions**: Some commands (e.g., `/reels create`) require `administrator=True`. Modify if you need different permissions.

---

## Contributing

1. **Fork** the repository.  
2. **Create** a new branch: `git checkout -b feature/some-feature`.  
3. **Commit** your changes: `git commit -m "Add some new feature"`.  
4. **Push** the branch: `git push origin feature/some-feature`.  
5. **Open a Pull Request** describing your changes.  

We welcome pull requests that improve documentation, code quality, or add relevant features!

---

## License

This project is licensed under the [MIT License](LICENSE).  
You’re free to use, modify, and distribute this code, as long as you preserve the original license notice.



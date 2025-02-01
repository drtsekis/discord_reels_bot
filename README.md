Below is a complete **`README.md`** file that you can copy and paste directly into your project. Feel free to adjust any sections or wording for your specific needs.

---

```markdown
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

- **Create Reels**: Users can upload a single image (PNG/JPG) that’s publicly viewable.  
- **Temporary Storage**: Each Reel remains active for 24 hours. After that, the bot removes both the Reel and associated likes.  
- **View Reels**: A simple “slideshow” interface (ephemeral to the viewer) that automatically navigates to the next Reel after 15 seconds of inactivity.  
- **User Likes**: Each user can like any Reel exactly once.  
- **Automated Cleanup**: A scheduled task runs every 10 minutes to remove expired Reels and their likes from the database.  
- **Slash Commands**: All functionality is accessed via Discord slash commands (e.g., `/reels create`, `/reels view`).  

---

## System Requirements

- **Python** 3.8 or above  
- **discord.py** 2.0+  
- **aiosqlite** (for asynchronous SQLite operations)  
- Optional: **python-dotenv** if you plan to load your token from a `.env` file  

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/discord-reels-bot.git
   ```
   Or download the project folder manually.

2. **Navigate into the Project Folder**:
   ```bash
   cd discord-reels-bot
   ```

3. **Create & Activate a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate     # On macOS/Linux
   venv\Scripts\activate        # On Windows
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Bot Token**  
   - Either edit `main.py` to include your bot token as a string.  
   - Or create a `.env` file in the root folder with `DISCORD_BOT_TOKEN=YourDiscordBotTokenHere`, and load it inside `main.py` with `python-dotenv`.

---

## Folder Structure

Below is an example of how you might organize the project. Adjust as needed:

```
discord_reels_bot/
├── cogs/
│   └── reels.py       # Cog containing the Reels feature code
├── data/
│   └── database.db    # SQLite database file (created automatically if not found)
├── main.py            # Main bot launcher (previously "bot.py")
├── requirements.txt   # Required Python libraries
├── .gitignore         # Files/folders to ignore in Git
└── README.md          # This documentation
```

### Key Points

- **`cogs/`**: Holds modular bot features (like Reels).  
- **`data/`**: Contains database files and other persistent data.  
- **`main.py`**: The entry point for running the bot.  
- **`.gitignore`**: Make sure `data/database.db` is ignored if you do not want to commit it.

---

## Usage

1. **Run the Bot**:
   ```bash
   python main.py
   ```
   If you configured `.env`, your bot token will be read from there.

2. **Invite the Bot** to your Discord server using the OAuth2 URL generated in the [Discord Developer Portal](https://discord.com/developers/applications).

### Commands Overview

- **`/reels create`**  
  Upload a new Reel by attaching a PNG or JPG.  
  - Each user can only upload **one** active Reel at a time.  
  - An ephemeral confirmation message is sent to the user.

- **`/reels view`**  
  View all available Reels in an ephemeral slideshow.  
  - **Previous** (`◀️`), **Next** (`▶️`) to navigate.  
  - **Like** (`❤️`) to like the current Reel.

- **`/reels terms`**  
  Shows the usage terms or guidelines for Reels in an ephemeral message.

### Example Workflow

1. **User** runs `/reels create` and uploads an image.  
2. The bot stores the Reel in the database, valid for 24 hours.  
3. Another **User** runs `/reels view` to browse Reels, then likes the new Reel.  
4. After 24 hours, the automated cleanup task removes expired Reels (and likes) from the database.

---

## Database Details

- Uses **SQLite** as its data store, typically `database.db` inside the `data` folder.  
- **Tables**:  
  - `reels`: Stores `id`, `user_id`, `image_url`, `datetime` (upload time), and `likes`.  
  - `reel_likes`: Stores `(user_id, image_url)` pairs to track likes.  
  - Optionally, other tables (like `duty`) for any custom logic.

**Retention**:  
- A background task (`@tasks.loop(minutes=10)`) deletes Reels older than 24 hours, plus any associated likes in `reel_likes`.

---

## Bot Configuration

Inside `main.py` (or your main launch file):

- **Command Prefix**: `'!'` is used if you need prefix-based commands. Slash commands are set up via app commands.  
- **Intents**: `discord.Intents.all()`. Make sure to enable the necessary intents in the [Developer Portal](https://discord.com/developers/applications).  
- **Token**:  
  - `bot.run("YOUR_BOT_TOKEN")`, or  
  - `bot.run(os.getenv("DISCORD_BOT_TOKEN"))` if using `.env`.

---

## Customization

1. **Folder/File Names**: Rename `cogs` to something else if you prefer; just update `main.py` references.  
2. **Language/Text**: All user-facing messages (in `reels.py`) can be edited for style or translated.  
3. **Cleanup Interval**: Currently 10 minutes; update `@tasks.loop(minutes=10)` to a different time if desired.  
4. **Reel Expiration**: Set to 24 hours by default (`86400` seconds). Change the `cutoff` logic in `clean_up_old_reels` as needed.  
5. **Auto-Switch Timer**: The 15s wait before auto-switching Reels is in `ReelsView.idle_logic()`. Adjust if you prefer a different interval.

---

## Known Issues & Limitations

- **One Reel per User**: The code restricts each user to one active Reel at a time. If you want multiple Reels per user, remove or change that logic.  
- **No GIFs**: The bot only allows static images (`image/png`, `image/jpeg`, `image/jpg`). Expand the content-type checks if needed.  
- **Ephemeral Viewing**: By default, `/reels view` is ephemeral, so only the user who triggered it sees the Reels. If you need a public channel display, remove `ephemeral=True` from follow-up calls.  
- **Administrator Permissions**: Some commands (create/view) require administrator permissions. Adjust those constraints to suit your server’s policy.

---

## Contributing

1. **Fork** the repository.  
2. **Create** a new branch: `git checkout -b feature/some-feature`.  
3. **Commit** your changes: `git commit -m "Add new feature"`.  
4. **Push** the branch: `git push origin feature/some-feature`.  
5. **Open a Pull Request** describing the changes you made.  

We welcome pull requests that improve code quality, documentation, or add relevant new features.

---

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this code in your own projects, provided you retain the original license terms.

---

*Happy coding! Feel free to add or edit any sections in this documentation to suit your project's needs.*
```

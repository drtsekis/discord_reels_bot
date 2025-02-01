# Discord Reels Bot

A **Discord bot** that provides a temporary “Reels” feature—users can upload images that remain active for 24 hours. Other users can view and like these images; the bot automatically removes them (and their associated likes) after expiration.

---

## Table of Contents

1. [Features](#features)  
2. [System Requirements](#system-requirements)  
3. [Installation](#installation)
4. [Usage](#usage)  

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
   git clone https://github.com/your-username/discord-reels-bot.git```
- Change Directory to the project folder:
   cd discord-reels-bot
- (Recommended) Create & Activate a Virtual Environment:
   ```bash python -m venv venv
   source venv/bin/activate       # On macOS/Linux
   venv\Scripts\activate          # On Windows```

- Change Directory to the project folder:
   cd discord-reels-bot
- Change Directory to the project folder:
   cd discord-reels-bot

---

## Usage

1. **Clone the Repository** (or download the folder):
   ```bash
   git clone https://github.com/your-username/discord-reels-bot.git

---

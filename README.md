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

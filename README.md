# VexFile Bot

This is a Telegram bot that supports multiple languages and offers user registration, login, and news management functionalities. The bot allows users to select their language and provides inline buttons for interaction.

## Features

- Multi-language support (English, Russian, Polish, Hindi, Arabic)
- User registration and login with inline buttons
- Admin commands for managing news and user statistics
- News broadcasting functionality to all users
- Deletion of the last bot message before sending a new one

## Setup

### Prerequisites

- Python 3.7+
- Telegram bot token from [@BotFather](https://t.me/BotFather)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/justoperator/vexfilebot.git
   cd vexfilebot

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

3. Configure the bot token and admin IDs:

   In the `config.py` file, add your bot token and admin ID:

   ```python
   token = 'PASTE YOUR API TOKEN FROM @BotFather'
   admns = [YOUR_TELEGRAM_ID]

4. Initialize the SQLite database:

   Run the database configurator to create the necessary tables:

   ```bash
   python database/configurator.py

#### Running the Bot

To start the bot, run:

    ```bash
    python main.py

## Admin Commands

- `/list` - Get the total number of registered users.
- `/addnews` - Add news that will be sent to all users.
- `/seenews` - View the latest news stored in the bot.
- `/news` - Send the latest news to all registered users.

## Language Support

The bot uses the following languages:

- English 🇬🇧
- Russian 🇷🇺
- Polish 🇵🇱
- Hindi 🇮🇳
- Arabic 🇸🇩

Users can select their preferred language during the start of their interaction with the bot.

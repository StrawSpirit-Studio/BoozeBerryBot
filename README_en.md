
# README

## Bot Description
This bot is designed to perform various tasks, including:
1. **Speech-to-Text (STT):** The bot can accept voice messages and convert them into text using speech recognition. This uses an AI model that is downloaded the first time you run the command.

## Purpose
The bot is created to simplify everyday tasks, provide information, and entertainment for users. It can be useful for those who want to perform speech recognition or use other useful features without the need to switch to other platforms that charge for such services.

## Installation and Setup

1. Clone the repository:
   ```
   git clone <your_repository_URL>
   cd <folder_name>
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. In the `config.py` file, provide your Telegram authorization details:
   - API_ID - Telegram API ID
   - API_HASH - Telegram API Hash
   - PHONE_NUMBER - Your phone number for Telegram authorization

   You can obtain these details from [my.telegram.org](https://my.telegram.org)

4. Run the bot:
   ```
   python main.py
   ```

## Available Commands

`$stt` - Speech-to-Text (Not tested on Linux and MacOS distros)  
`$ping` - Check bot availability and display server info  
`$cat` - Send random cat images. [Requires an API key for access](https://thecatapi.com/) (API key must be specified in the config file)  
`$sping` - Check server availability  
`$speedtest` - Perform a speed test for your internet connection  
`$8ball` - Answers to questions in the style of a "magic 8 ball"  
`$tracert` - Perform a route trace to a server  
`$calc` - Perform simple mathematical calculations (may be unstable)  
`$screen` - Capture and send a screenshot (does not work without a graphical interface)  
`$lock` - Lock the screen  
`$sleep` - Put the system to sleep mode  
`$hibernate` - Put the system into hibernation mode  
`$spotify` - Launch Spotify and automatically play the last song  

## Using the stt Command

1. Before using the `stt` command, manually download **ffmpeg version 8.0 or later** and place it in the folder `packages/ffmpeg/bin/ffmpeg.exe`.

2. Make sure the folder is named `ffmpeg` and located in the `packages` folder.

3. The first time you run the command, the bot will download the AI model, which may take some time.

## Minimum Requirements for STT

- Processor: Intel i7-11th gen or AMD Ryzen 5 3600
- RAM: 16 GB
- Disk Space: 5 GB

## Recommended Specifications

- Processor: Intel i9-11th gen or AMD Ryzen 7 5800X
- RAM: 32 GB
- Disk Space: 5 GB
- Graphics Card: NVIDIA GeForce RTX 3060 or AMD Radeon RX 6700 XT

## STT Configuration
In the `config.py` file, you can configure parameters for STT.

- `whisper_presets`: Supported options: `accurate`, `fast`, `normal`, `custom`.

  - `accurate` - Most accurate but slowest.
  - `fast` - Fastest but least accurate.
  - `normal` - A mix of accuracy and speed.
  - `custom` - Custom mode, allowing you to set your own Whisper parameters.

- `beam_size`: Controls how many options Whisper will consider.
- `best_of`: Controls how many options Whisper will consider.
- `temperature`: Controls the randomness of the result.

### License
This project is distributed under the MIT License.  
License details: [LICENSE](LICENSE)

## Author
This project is created and maintained by [@strawspirit_studio](https://t.me/strawspirit_studio)  
Bot's creator - [@nestor_churin](https://t.me/really_hilariousn)

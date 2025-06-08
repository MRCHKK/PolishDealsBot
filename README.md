# Polish Card Deals Discord Bot

Discord bot for aggregating and monitoring car offers from multiple Polish automotive marketplaces.

## Features

- **Multi-source scraping**: Monitors offers from Otomoto, Lento, Autoplac, and Sprzedajemy
- **Real-time notifications**: Sends new offers to Discord channel immediately
- **Duplicate detection**: Tracks sent offers to avoid duplicates
- **Configurable search**: Customize location, radius, and price limits
- **Professional architecture**: Clean, maintainable code with proper separation of concerns
- **Async processing**: Efficient concurrent scraping of multiple sources
- **Error resilience**: Retry mechanisms and graceful error handling
- **Logging**: Comprehensive logging to both file and Discord

## Setup
### 1. Clone repository.
```git clone [LINK]```

### 2. Create virtual environment
```python -m venv venv ```  
```source venv/bin/activate ```

### 3. Install dependencies
``` pip install -r requirements.txt ```

### 4. Configure environment
``` cp .env.example .env ```  
Edit .env with your Discord token and preferences

### 5. Run the bot
```python -m src.main```


## Configuration
Edit .env file to customize:

DISCORD_TOKEN: Your Discord bot token   
DISCORD_CHANNEL_ID: Channel ID for notifications  
SEARCH_LOCATION: City to search in (default: Siedlce)  
SEARCH_RADIUS_KM: Search radius in kilometers  
MAX_PRICE: Maximum price filter  
UPDATE_INTERVAL_SECONDS: How often to check for new offers

## Docker Support
Run with Docker Compose:
```bashdocker-compose up -d```

## Contact
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/emilmar/) [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MRCHKK) [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:emil.marcz@gmail.com)
## Built With
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/Discord.py-2.3.2-blue?style=for-the-badge&logo=discord&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-Web%20Scraping-59666C?style=for-the-badge)
![Requests](https://img.shields.io/badge/Requests-HTTP%20Client-FF6B6B?style=for-the-badge)
![Aiohttp](https://img.shields.io/badge/Aiohttp-Async%20HTTP-00BAFF?style=for-the-badge)


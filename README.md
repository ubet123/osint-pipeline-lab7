# OSINT Lab 7 - Automated Social Media OSINT Pipeline

## Project Overview
This project implements an automated OSINT pipeline that collects, processes, and analyzes social media data from multiple platforms including Reddit, GitHub, and Twitter.

## Features
- Multi-platform data collection (Reddit, GitHub, Twitter)
- Automated data cleaning and preprocessing
- Sentiment analysis using TextBlob
- SQLite database storage
- Scheduled automated collection

## Setup Instructions
```
1.Clone the repository
git clone <your-repo-url>
cd osint_pipeline

2.Create virtual environment:
python -m venv osint_env
source osint_env/bin/activate  # Linux/Mac
osint_env\Scripts\activate    # Windows

3.Install Dependencies:
pip install -r requirements.txt

4.Set up environment variables:
cp sample.env.example .env
# Edit .env with your API keys

5.Run the pipeline:
python main_safe.py

```

## API Keys Required
Twitter API Bearer Token

Reddit Client ID and Secret

GitHub Personal Access Token (optional)

## Project Structure
```
osint_pipeline/
├── collectors/          # Platform-specific data collectors
├── utils/              # Utilities for processing
├── data/               # Database and generated files
├── screenshots/        # Evidence screenshots
├── main_safe.py        # Main pipeline
└── requirements.txt    # Dependencies
```


## Screenshots

| Project | Screenshot |
| ------- | ---------- |
| Database Records | ![Screenshot 1]('../osint_pipeline/screenshots/Screenshot%202025-09-19%20123256.png') ![Screenshot 2](../osint_pipeline/screenshots/Screenshot%202025-09-19%20123316.png) ![Screenshot 3](../osint_pipeline/screenshots/Screenshot%202025-09-19%20123332.png) ![Screenshot 4](../osint_pipeline/screenshots/Screenshot%202025-09-19%20123403.png) |
| Sentiment Chart | ![Sentiment](../osint_pipeline/screenshots/sentiment_distribution.png) ![Platform](../osint_pipeline/screenshots/platform_distribution.png) |
| API Success | ![API](../osint_pipeline/screenshots/Screenshot%202025-09-19%20123227.png) |


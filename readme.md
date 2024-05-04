# Reddit Karma Farmer

Welcome to Reddit Karma Farmer, a sophisticated tool designed to help you efficiently manage and enhance your Reddit karma points. This application automates the process of engaging with Reddit posts, generating comments that align with popular trends and user sentiments, thereby increasing the likelihood of receiving upvotes.

## Getting Started

To run the karma farmer locally using the terminal, follow these steps:

1. Navigate to the project directory.
2. Run the `app.py` file.

```bash
python app.py
```

To run the farmer with a web interface locally, follow these steps:

1. Navigate to the project directory.
2. Run the `index.py` file.
3. Visit the `/start_bot` route to initiate the karma farmer.
4. Access the `/log` page to view detailed logs.

```bash
python index.py
```

To deploy the farmer on hosting services like Render and more, configure the hosting server to execute `web.py`.
Render and hugging face spaces recommended!
## Features

- **Effortless Engagement**: Automatically engage with Reddit posts by generating comments that resonate with the community's interests.
- **User-Friendly Interface**: Access the karma farmer through a web interface for convenient interaction and monitoring.
- **Scalable Deployment**: Deploy the farmer on various hosting platforms to ensure accessibility and scalability.

## Requirements

- Python 3.7 or higher
- PRAW (Python Reddit API Wrapper)
- Fake Useragent
- Flask (for web interface)
- chipling ai (optional, for comment generation)

## Configuration

Ensure to configure the following parameters in the `config.py` file:

- `client_id`: Reddit API client ID
- `client_secret`: Reddit API client secret
- `username`: Reddit account username
- `password`: Reddit account password
- `webhook`: Discord webhook URL for logging (optional)
- `discord_webhook`: Boolean indicating whether Discord webhook is enabled (optional)
- `type`: Comment generation method (e.g., "karma" for using the language model, "ad" for using predefined comments)

## Usage

1. Configure the `config.py` file with your Reddit account credentials and other settings.
2. Run the application using either the terminal or a web interface.
3. Monitor the logs to track the farmer's activities and engagement.
4. Customize the comment generation method and parameters based on your preferences and requirements.

## Disclaimer

This application is intended for educational and experimental purposes only. Use it responsibly and adhere to Reddit's guidelines and terms of service. Excessive automation and misuse may lead to account suspension or other penalties imposed by Reddit.

# Homestar Platform Scraper

A Python-based web scraping tool designed to extract company information from Homestar.com. This scraper navigates through different service categories and subcategories to collect detailed business information.

## Features

- Automated navigation through service categories and subcategories
- Dynamic content loading through scroll detection
- Company information extraction
- Anti-detection measures using undetected-chromedriver
- Detailed logging system
- Configurable category structure via JSON

## Prerequisites

- Python 3.8+
- Chrome browser installed
- Python virtual environment (recommended)

## Installation

1. Clone the repository and navigate to the project directory:
```

## Configuration

The scraper uses a JSON configuration file (`config/categories.json`) to define the categories and subcategories to scrape. The structure follows this format:
```json
{
  "Category Name": [
    {
      "Subcategory Name": "URL"
    }
  ]
}
```

## Usage

Run the scraper using:
```bash
python src/main.py
```

The scraper will:
1. Initialize the Chrome driver with anti-detection measures
2. Load categories from the configuration file
3. Navigate through each category and subcategory
4. Extract company information
5. Log the progress and results

## Logging

The scraper maintains two types of log files in the `logs` directory:
- `latest.log`: Contains the most recent scraping session logs
- `scraper_TIMESTAMP.log`: Archived logs for each scraping session

## Project Structure

```
homestar/
├── config/
│   └── categories.json     # Scraping configuration
├── src/
│   ├── main.py            # Main script
│   ├── scraper.py         # Scraping functions
│   ├── utils.py           # Utility functions
│   └── requirements.txt    # Dependencies
├── logs/                   # Log files
└── README.md
```

## Dependencies

- selenium
- beautifulsoup4
- requests
- undetected-chromedriver

## Error Handling

The scraper includes robust error handling for:
- Invalid subcategory formats
- Network issues
- Anti-bot detection
- Page loading failures

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request



# Email Extractor

A Python-based web scraping tool that strategically extracts and validates email addresses from websites. The tool intelligently searches through main pages and contact pages, prioritizing business-relevant email addresses.

## Features

- Automated email extraction from websites
- Smart contact page detection
- Email validation and cleaning
- Priority-based email selection
- MX record verification
- Detailed logging system
- Anti-detection measures using undetected-chromedriver

## Prerequisites

- Python 3.8+
- Chrome browser installed
- Python virtual environment (recommended)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sowasred/cold-call.git
cd cold-call/email-extractor
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```


4. Add target websites to `config/websites.json`:

```json
[
  "https://example.com",
  "https://example.org"
]
```

5. Run the script:

```bash
python3 src/main.py
```

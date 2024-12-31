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
- In-place CSV enrichment with email data

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

## Usage

1. Place your CSV file in the `output` directory. The CSV file should contain at least these columns:
   - `Company Name`: Name of the company
   - `Website`: Company's website URL

Example CSV format:
```csv
Company Name,Website
Example Corp,https://example.com
Test Company,https://test-company.com
```

2. Run the script:

```bash
python3 src/main.py
```

## CSV Processing Details

The script will:

- The tool processes the most recent CSV file in the `output` directory
- The original file is updated in-place with email data
- If a website already has an associated email, it will be updated if a better match is found
- Failed email extractions will be logged but won't affect other entries
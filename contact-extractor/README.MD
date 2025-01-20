# Contact Extractor

A Python-based web scraping tool that strategically extracts and validates business contact information from websites. The tool intelligently searches through main pages and contact pages, prioritizing business-relevant contact details like emails and phone numbers.

## Features

- Automated contact information extraction from websites
  - Email addresses
  - Phone numbers (Canadian 10-digit format)
- Smart contact page detection and prioritization
- Comprehensive validation and cleaning
  - Email format and domain validation with MX record verification
  - Canadian phone number format validation
- Priority-based selection system
  - Business-relevant email addresses (e.g., info@, contact@)
  - Standard Canadian phone number format (XXX-XXX-XXXX)
- Anti-detection measures using undetected-chromedriver
- Detailed logging system
- In-place CSV enrichment with contact data

## Prerequisites

- Python 3.8+
- Chrome browser installed
- Python virtual environment (recommended)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sowasred/cold-call.git
cd cold-call/contact-extractor
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r src/requirements.txt
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

## How It Works

The tool employs a strategic approach to contact information extraction:

1. **Main Page Scan**
   - Scans the website's main page for contact information
   - Extracts emails and phone numbers using specialized patterns
   - Validates and scores found contact details

2. **Contact Page Detection**
   - If needed, identifies potential contact pages using common keywords
   - Analyzes links containing terms like "contact", "about", "reach-us"
   - Supports multiple languages (e.g., "kontakt" for German)

3. **Data Validation**
   - **Emails**:
     - Validates format and domain
     - Verifies MX records
     - Filters disposable and test addresses
   - **Phone Numbers**:
     - Validates Canadian 10-digit format
     - Handles numbers with leading '1'
     - Filters test and invalid numbers

4. **Priority Selection**
   - **Emails**: Prioritizes based on:
     - Domain match with website
     - Business-relevant patterns
     - Valid MX records
   - **Phone Numbers**:
     - Ensures standard Canadian format
     - Removes leading '1' if present
     - Filters invalid and test numbers

## CSV Processing Details

The script processes files as follows:

- Automatically selects the most recent CSV in the `output` directory
- Updates the original file in-place with contact data
- Preserves existing data while updating with better matches if found
- Handles failures gracefully without affecting other entries

- Failed extractions are logged but don't stop the process
- Invalid websites or timeouts are handled gracefully
- Detailed logs are maintained for debugging
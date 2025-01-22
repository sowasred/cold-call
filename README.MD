# Business Development Automation Suite

A comprehensive monorepo containing tools for automated business development and outreach. This suite includes tools for data extraction, email harvesting, and personalized outreach automation.

## Overview

This repository contains four main components that work together in sequence for automated business development:

1. **Platform Scrapers**: Collection of specialized scrapers for various business platforms (currently supporting Homestar), designed to:
   - Extract company information from business directories
   - Generate CSV files with company details (name, website, industry, etc.)
   - Easily extensible for additional platforms
   
2. **Contact Extractor**: A Python-based tool that enriches the scraped data by:
   - Visiting each company's website
   - Extracting missing contact information (email, phone, address)
   - Updating the CSV with complete company information

3. **Marketing Email Generator**: An AI-powered system that:
   - Takes two inputs:
     - `sender.csv`: Information about your company
     - `targets.csv`: Enriched company data from previous steps
   - Uses multiple AI agents to:
     - Research target companies
     - Analyze company websites
     - Generate personalized email content
   - Outputs a JSON file containing tailored marketing emails each company existed in targets.csv

4. **Email Sender**: Automated email dispatch system that:
   - Processes the generated email JSON file
   - Handles email delivery to target companies
   - Manages sending limits and tracking

## Workflow

1. **Lead Generation**:
   - Run platform scrapers to collect initial company data
   - Output: CSV file with basic company information

2. **Contact Enrichment**:
   - Process the scraped data through contact extractor
   - Output: Enriched CSV with complete contact details

3. **Email Generation**:
   - Prepare sender.csv with your company information
   - Use enriched company data as targets.csv
   - Run marketing email generator
   - Output: JSON file with personalized emails

4. **Email Distribution**:
   - Process the email JSON file
   - Send personalized emails to target companies

## Setup and Usage

Each component has its own setup instructions and requirements. Please refer to the individual README files in each project directory:

- [Platform Scrapers Documentation](platform-scrapers/README.md)
- [Contact Extractor Documentation](contact-extractor/README.md)
- [Marketing Email Generator Documentation](marketing-email-generator/README.md)
- [Email Sender Documentation](email-sender/README.md)

## Other Projects:
1. **sitemap-data-harvester**
This is a web application that extracts and analyzes company data from website sitemaps. Features include:
- XML sitemap parsing
- Content extraction
- AI-powered company summary generation

2. **lead-reach**
A modern Next.js-based SaaS platform designed to streamline lead generation and email marketing. Companies can:
- Register and manage their business profile
- Access targeted lead generation tools
- Create and send personalized email campaigns
- Track engagement and campaign performance
- Scale their outreach efforts efficiently
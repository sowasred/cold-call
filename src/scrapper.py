from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
import json
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_driver():
    """Initialize and return the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def scroll_to_load(driver, subcategory_name):
    """Scroll to the bottom of the page until all content is loaded."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Check for pagination element that indicates bottom of page
        pagination_element = driver.find_elements(By.CLASS_NAME, "pagination-wrap--small")
        if pagination_element:
            logger.info(f"Found pagination element - reached bottom of page for {subcategory_name}")
            break
            
        if new_height == last_height:
            logger.info(f"Reached bottom of page since height is the same for {subcategory_name}")
            break
        last_height = new_height


def extract_companies(driver):
    """Extract companies with reviews and a valid score from the loaded page."""
    company_name_urls = []
    try:
        company_links = driver.find_elements(By.CSS_SELECTOR, ".company-result .name-row-text__text")
        for company in company_links:
            try:
                name = company.text
                url = company.get_attribute("href")
                company_name_urls.append({"name": name, "url": url})
            except Exception as e:
                logger.warning(f"Failed to parse company: {e}")
    except NoSuchElementException:
        logger.error("No companies found on the page.")
    return company_name_urls


def fetch_company_details(driver, company_name_urls):
    """Fetch website and phone number for a given company URL."""
    for company in company_name_urls:
        try:
            driver.get(company['url'])
            # Wait up to 10 seconds for page to load
            # wait = WebDriverWait(driver, 10)
            
            # # Wait for and click the reveal phone button
            # reveal_button = wait.until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='reveal-phone-number']"))
            # )
            # reveal_button.click()
            time.sleep(1)  # Short wait for phone number to appear
            
            # phone_number = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='company-phone-number'] span").text
            # get the website
            website = driver.find_element(By.CSS_SELECTOR, "a[data-testid='company-listing-website']").get_attribute("href")
            # get the score of the company
            score = driver.find_element(By.CSS_SELECTOR, "p.star-score-icon-and-score__text").text
            print('website', website)
            print('score', score)
            # Get social media links
            social_links = {}
            try:
                # Check for Instagram
                instagram = driver.find_element(By.CSS_SELECTOR, "a[data-testid='instagram']")
                social_links['instagram'] = instagram.get_attribute("href")
            except NoSuchElementException:
                pass

            try:
                # Check for Facebook 
                facebook = driver.find_element(By.CSS_SELECTOR, "a[data-testid='facebook']")
                social_links['facebook'] = facebook.get_attribute("href")
            except NoSuchElementException:
                pass

            try:
                # Check for Twitter
                twitter = driver.find_element(By.CSS_SELECTOR, "a[data-testid='twitter']")
                social_links['twitter'] = twitter.get_attribute("href")
            except NoSuchElementException:
                pass

            try:
                # Check for LinkedIn
                linkedin = driver.find_element(By.CSS_SELECTOR, "a[data-testid='linkedin']")
                social_links['linkedin'] = linkedin.get_attribute("href")
            except NoSuchElementException:
                pass

            print(social_links)
            company['social_links'] = social_links
            company['phone_number'] = phone_number
            company['website'] = website
            company['score'] = score
        except TimeoutException:
            logger.error(f"Timeout waiting for elements on page for company: {company['name']}")
            continue
        except Exception as e:
            logger.error(f"Error processing company {company['name']}: {str(e)}")
            continue
            
    return company_name_urls


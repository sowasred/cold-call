from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging

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
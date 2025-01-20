import undetected_chromedriver as uc
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
logger = logging.getLogger()

def initialize_driver():
    """Initialize and return the Selenium WebDriver."""
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    )
    options.add_argument("--window-size=1440,900")

    return uc.Chrome(options=options)


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
            logger.info(f"Navigating to company URL: {company['url']}")
            
            # Wait for page to be fully loaded
            logger.debug("Waiting for page load...")
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            logger.info("Page load complete")

            # Log detailed page information
            logger.info(f"Current URL: {driver.current_url}")
            logger.info(f"Page Title: {driver.title}")
            
            # Stop here for inspection
            # input("Press Enter to continue after inspecting the page...")
            
            # Check if we can find any main content
            try:
                # Wait for page load
                # WebDriverWait(driver, 10).until(
                #     lambda driver: driver.execute_script('return document.readyState') == 'complete'
                # )
                
                # Log the current page title and URL for verification
                # Uncomment the following lines one by one to debug step by step
                
                # Step 1: Log the page title
                logger.debug(f"Page Title: {driver.title}")
                
                # Step 2: Log the current URL
                logger.debug(f"Current URL: {driver.current_url}")
                
                # Step 3: Log all available IDs on the page
                contact_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-react-class='CompanyContactLinks']"))
                )
                logger.debug("Found element with data-react-class='CompanyContactLinks'")
                logger.debug(f"Element HTML: {contact_element.get_attribute('innerHTML')}")
                
                # # Step 4: Try to find main content with different approaches
                # main_content = WebDriverWait(driver, 5).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, ".company-result"))
                # )
                # logger.debug("Main content found using alternative selector")
                
                # # Log all available IDs on the page
                # ids = driver.execute_script("""
                #     return Array.from(document.querySelectorAll('[id]')).map(el => el.id);
                # """)
                # logger.debug(f"Available IDs on page: {ids}")
                
                # # Try to find main content with different approaches
                # main_content = WebDriverWait(driver, 5).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, ".company-result"))
                # )
                # logger.debug("Main content found using alternative selector")
                
            except TimeoutException:
                logger.error("Could not find main content - possible anti-bot protection")
                logger.error(f"Page source preview: {driver.page_source[:1000]}")
                raise Exception("Possible anti-bot protection")

            # Now proceed with finding the button
            try:
                logger.debug("Attempting to find reveal button...")
                reveal_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='reveal-phone-number']"))
                )
                
                # Log page state before clicking
                logger.debug(f"Page title: {driver.title}")
                logger.debug(f"Current URL: {driver.current_url}")
                
                reveal_button.click()
                logger.info("Successfully clicked reveal button")
                
                try:
                    # Wait for the element containing data-react-props
                    contact_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-react-class='CompanyContactLinks']"))
                    )
                    
                    # Get the data-react-props attribute
                    props_json = contact_element.get_attribute('data-react-props')
                    
                    # Parse the JSON (need to handle HTML entities)
                    import html
                    decoded_props = html.unescape(props_json)
                    import json
                    props_data = json.loads(decoded_props)
                    
                    # Extract phone number
                    phone_number = props_data.get('phoneNumber')
                    logger.info(f"Successfully extracted phone number: {phone_number}")
                    
                except TimeoutException:
                    logger.error("Could not find CompanyContactLinks element")
                    phone_number = None
                except json.JSONDecodeError:
                    logger.error("Failed to parse data-react-props JSON")
                    phone_number = None
                except Exception as e:
                    logger.error(f"Unexpected error while extracting phone number: {str(e)}")
                    phone_number = None
                
            except TimeoutException as e:
                logger.error(f"TimeoutException: {str(e)}")
                # Log more detailed page state
                logger.error("Current URL: " + driver.current_url)
                logger.error("Page title: " + driver.title)
                logger.error("Cookies: " + str(driver.get_cookies()))
                phone_number = None
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                logger.error(f"Error type: {type(e).__name__}")
                phone_number = None
            
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


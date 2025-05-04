from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import sys
import json

# Store original print function
orig_print = print

# Disable printing large HTML chunks by limiting output size
def limited_print(*args, **kwargs):
    """Wrapper for print that limits the size of string outputs"""
    modified_args = []
    for arg in args:
        if isinstance(arg, str) and len(arg) > 200:
            modified_args.append(arg[:200] + "... [output truncated]")
        else:
            modified_args.append(arg)
    # Use the original print function, not the overridden one
    orig_print(*modified_args, **kwargs)

# Replace the standard print function with our limited version
print = limited_print

# Error handling decorator
def safe_web_operation(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)[:200]}")
            return None
    return wrapper

# Login credentials - Replace these with your actual credentials
EMAIL = ""  # Replace with your email
PASSWORD = ""         # Replace with your password

# List of profiles to check - these are the ones you suspect of fake reviews
profile_names = [
    # Add profile names here
    # Examples:
    # 'profile1',
    # 'profile2',
]

# Convert profile names to full URLs
profile_urls = [f'https://www.kaufmich.com/p/{name}/reviews' for name in profile_names]

# Function to scroll and load all reviews
@safe_web_operation
def scroll_and_load_all_reviews(driver):
    print("Starting to scroll and load all reviews...")
    last_review_count = 0
    max_scroll_attempts = 10  # Reduced from 15 to 5
    scroll_attempts = 0
    
    while scroll_attempts < max_scroll_attempts:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Scrolled down (attempt {scroll_attempts + 1})")
        
        # Wait for potential new content to load
        time.sleep(random.uniform(2, 3))
        
        # Get the current number of reviews
        review_items = driver.find_elements(By.CLASS_NAME, 'review-item')
        current_count = len(review_items)
        print(f"Found {current_count} reviews after scrolling")
        
        # If no new reviews were loaded, increment attempt counter or exit early
        if current_count == last_review_count:
            scroll_attempts += 1
            print(f"No new reviews found (attempt {scroll_attempts}/{max_scroll_attempts})")
            
            # Try one more random scroll to trigger potential loading
            random_scroll = random.randint(500, 1000)
            driver.execute_script(f"window.scrollBy(0, {random_scroll});")
            time.sleep(1)
            
            # Check again after the random scroll
            review_items = driver.find_elements(By.CLASS_NAME, 'review-item')
            if len(review_items) == current_count:
                # Still no new reviews, exit early if we've made at least 2 attempts
                if scroll_attempts >= 2:
                    print("No new reviews after multiple attempts, exiting scroll loop early")
                    break
        else:
            # Reset counter if we found new reviews
            scroll_attempts = 0
            last_review_count = current_count
            print(f"Found new reviews, continuing to scroll")
            
    print(f"Finished scrolling, found total of {last_review_count} reviews")
    return last_review_count

# Process and extract reviews
@safe_web_operation
def extract_reviews(html_content, profile_name):
    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Check for empty state message
    empty_state = soup.find('div', class_='placeholder-empty-tip')
    if empty_state:
        print("No reviews found. Message:", empty_state.text.strip())
        return []
        
    # Find all review items
    review_items = soup.find_all('li', class_='review-item')
    print(f"Extracting data from {len(review_items)} reviews")
    
    review_data = []
    
    # Extract data from each review item
    for i, review in enumerate(review_items):
        try:
            # Try to extract the reviewer profile link
            reviewer_link = review.select_one('.review-item__other-header a.avatar')
            
            # Try to extract the review date
            date_element = review.select_one('.review-item__separator-date')
            review_date = date_element.text.strip() if date_element else "Date not found"
            
            # Extract the review content
            content_element = review.select_one('.review-item__other-content')
            review_content = content_element.text.strip() if content_element else "No content found"
            
            # Count the number of stars - only from the other section (reviewer's rating)
            rating_div = review.select_one('.review-item__other .review-item__rating .rating')
            if rating_div:
                stars = rating_div.select('i.kmt.kmt-star-full.star-size-s')
                star_count = len(stars)
            else:
                star_count = 0
            
            if reviewer_link and reviewer_link.has_attr('href'):
                profile_href = reviewer_link['href']
                print(f"Review #{i+1} - Profile: {profile_name}, Reviewer: {profile_href}, Stars: {star_count}, Date: {review_date}")
                
                review_data.append({
                    "name": profile_name,
                    "reviewed_by_profile": profile_href,
                    "review_date": review_date,
                    "review_content": review_content,
                    "star_count": star_count
                })
            else:
                print(f"Review #{i+1}: Could not find reviewer profile link")
        except Exception as e:
            print(f"Error processing review #{i+1}: {str(e)[:100]}")
            
    return review_data

# Main function to process all profiles
def process_all_profiles(profile_urls):
    all_review_data = []
    
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Log in first
        print("Loading main page...")
        driver.get('https://www.kaufmich.com')
        time.sleep(3)

        # Handle cookie banner
        try:
            cookie_buttons = driver.find_elements(By.XPATH, "//div[contains(@id, 'cookie') and contains(text(), 'akzeptieren')]")
            if cookie_buttons:
                print("Accepting cookies...")
                cookie_buttons[0].click()
                time.sleep(2)
        except Exception as e:
            print(f"Error handling cookie banner: {e}")

        # Login
        try:
            print("Looking for login button...")
            login_buttons = driver.find_elements(By.XPATH, "//span[contains(text(), 'Log in')]")
            if login_buttons:
                print("Clicking login button...")
                login_buttons[0].click()
                time.sleep(3)
        except Exception as e:
            print(f"Error finding login button: {e}")

        try:
            print("Attempting to log in...")
            # Look for username/email field
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='login-widget-username-input']"))
            )
            email_field.send_keys(EMAIL)
            time.sleep(1)

            # Password field
            password_field = driver.find_element(By.CSS_SELECTOR, "input[data-testid='login-widget-password-input']")
            password_field.send_keys(PASSWORD)
            time.sleep(1)

            # Invisible login checkbox
            try:
                invisible_login_checkbox = driver.find_element(By.XPATH, "//span[contains(text(), 'Unsichtbar einloggen')]/preceding-sibling::span/i")
                invisible_login_checkbox.click()
                print("Checked 'Unsichtbar einloggen' option")
                time.sleep(1)
            except Exception as e:
                print(f"Could not check invisible login box: {e}")

            # Submit login
            submit_button = driver.find_element(By.CSS_SELECTOR, "div[data-testid='login-widget-login-button']")
            submit_button.click()
            time.sleep(5)
            
            if "login" not in driver.current_url.lower():
                print("Login appears successful")
            else:
                print("Login might have failed, but continuing anyway...")
        except Exception as e:
            print(f"Error during login process: {e}")

        # Process each profile URL
        for url in profile_urls:
            try:
                # Extract profile name from URL
                profile_name = url.split('/p/')[1].split('/')[0] if '/p/' in url else "unknown"
                
                print(f"\nProcessing profile: {profile_name}")
                print(f"Navigating to: {url}")
                driver.get(url)
                time.sleep(random.uniform(3, 5))

                # Scroll and load all reviews
                scroll_and_load_all_reviews(driver)

                # Extract reviews
                html_content = driver.page_source
                profile_reviews = extract_reviews(html_content, profile_name)
                
                # Add to all reviews
                all_review_data.extend(profile_reviews)
                print(f"Extracted {len(profile_reviews)} reviews for {profile_name}")
                
            except Exception as e:
                print(f"Error processing URL {url}: {str(e)[:200]}")

        # Save the review data to a JSON file
        with open('review_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_review_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nSaved {len(all_review_data)} reviews to review_data.json")

    except Exception as e:
        print(f"An error occurred in the main execution: {str(e)[:200]}")

    finally:
        # Pause before closing the browser
        input("Press Enter to close the browser...")
        
        # Close the browser
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    process_all_profiles(profile_urls)
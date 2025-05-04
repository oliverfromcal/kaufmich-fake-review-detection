# Review Scraper for Kaufmich.com

This tool helps analyze reviews to identify authentic and fake profiles on Kaufmich.com by collecting review data for analysis.

## Setup Guide

### 1. Setup Python

- Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
- Verify installation by opening a terminal and running:
  ```
  python --version
  ```

### 2. Install Required Dependencies

- Install Google Chrome browser if not already installed
- Install required packages:
  ```
  pip install selenium beautifulsoup4
  ```

- Install ChromeDriver:
  - On macOS with Homebrew:
    ```
    brew install chromedriver
    ```
  - On Windows/Linux: Download from [ChromeDriver website](https://chromedriver.chromium.org/downloads) matching your Chrome version
  - On macOS, if you get a security warning:
    ```
    xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
    ```

### 3. Collect Authentic Reviews

- Edit `hello.py` and uncomment authentic profiles in the `profile_names` list:
  ```python
  profile_names = [
      # authentic
      'emily_girlfriend',
      'lara_xoxo26',
      'whitealaska9',
      
      # fake
      # 'abitur2023',
      # ...
  ]
  ```
- If needed, update login credentials in the `EMAIL` and `PASSWORD` variables
- Run the script:
  ```
  python hello.py
  ```
- The script will save authentic reviews to `review_data.json`
- Rename the file to preserve the data:
  ```
  mv review_data.json authentic_reviews.json   # Linux/Mac
  rename review_data.json authentic_reviews.json   # Windows
  ```
- Verify data by checking that `authentic_reviews.json` contains review entries

### 4. Collect Fake Reviews

- Edit `hello.py` and update the `profile_names` list to only include fake profiles:
  ```python
  profile_names = [
      # authentic
      # 'emily_girlfriend',
      # ...
      
      # fake
      'abitur2023',
      'theresa-abiturientin',
      'blond-studentin',
      # ...
  ]
  ```
- Run the script:
  ```
  python hello.py
  ```
- Rename the output file:
  ```
  mv review_data.json fake_reviews.json   # Linux/Mac
  rename review_data.json fake_reviews.json   # Windows
  ```

### 5. Analyze a Profile in Question

- Edit `hello.py` to include only the profile you want to analyze:
  ```python
  profile_names = [
      'profile_to_analyze'
  ]
  ```
- Run the script:
  ```
  python hello.py
  ```
- This will create a new `review_data.json` with only data from that profile

### 6. Use LLM to Analyze the Data

- Upload the following files to an LLM (like ChatGPT, Claude, etc.):
  - `authentic_reviews.json`
  - `fake_reviews.json`
  - `review_data.json` (containing the profile in question)

- Ask the LLM to analyze the patterns and give feedback:
  ```
  Based on the patterns in authentic_reviews.json and fake_reviews.json, please analyze 
  review_data.json and tell me if this profile shows characteristics of authentic or fake reviews.
  What specific patterns did you identify that support your conclusion?
  ```

- **Time-Saving Option**: you can skip steps 3-4 and use existing `authentic_reviews.json` and `fake_reviews.json` files to directly analyze new profiles. This is useful if you want to quickly test the LLM analysis without collecting all the training data.

## Notes

- The script handles pagination by scrolling to load additional reviews
- Star ratings are extracted from the reviewer's rating section
- All data is saved with timestamps and full review content
- Login is required to access most profiles' reviews

## Troubleshooting

- If you encounter ChromeDriver errors, make sure your Chrome browser version matches your ChromeDriver version
- If you get security warnings on macOS, run the command in step 2 to remove quarantine attributes
- For login issues, verify your credentials and check if the site's login process has changed

## Additional Tips

- **Data Structure**: Each review contains profile name, reviewer link, date, content and star count
- **Recovery**: If script crashes, restart with fewer profiles at once
- **Rate Limiting**: Add delays between profiles to avoid IP blocks
- **Captchas**: If captchas appear, slow down scraping or use a different IP
- **Analysis Patterns**: Look for similar reviewers, identical text, unusual timing
- **Large Profiles**: Profiles with many reviews may take several minutes to scrape
- **Legal Note**: Use responsibly and in accordance with site terms of service 
# Kaufmich Fake Review Detection

This project analyzes reviews from Kaufmich.de to detect potential fake reviews using pattern matching and AI analysis.

## Features

- Scrapes reviews from Kaufmich.de profiles
- Analyzes review patterns using reference data
- Uses Perplexity AI to detect fake review patterns
- Compares against known authentic and fake review datasets

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Perplexity API key (get it from https://www.perplexity.ai/)
- Kaufmich.de account

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd kaufmich-fake-review-detection
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Required Packages

The following packages are required and will be installed via requirements.txt:
- selenium
- beautifulsoup4
- openai
- requests

## Configuration

1. Set your Perplexity API key as an environment variable:
```bash
export PERPLEXITY_API_KEY='your-api-key-here'
```

2. Set your Kaufmich.de credentials as environment variables:
```bash
export KAUFMICH_USERNAME='your-username'
export KAUFMICH_PASSWORD='your-password'
```

Or you can enter them when prompted by the script.

## Usage

1. Run the script:
```bash
python hello.py
```

The script will:
- Scrape reviews from the specified profiles
- Save the reviews to `review_data.json`
- Analyze the reviews using Perplexity AI
- Compare patterns with reference data from `authentic.json` and `fake.json`
- Display the analysis results

## Reference Data

The project uses two reference datasets:
- `authentic.json`: Contains examples of authentic reviews
- `fake.json`: Contains examples of fake reviews

These files are used to train the AI model to recognize patterns in reviews.

## Output

The script generates:
- `review_data.json`: Contains the scraped reviews
- Analysis results in the console showing whether the reviews appear authentic or fake

## Error Handling

The script includes error handling for:
- Network issues
- Missing API keys
- Invalid profile URLs
- Browser automation failures
- Missing credentials

## Security Notes

- Never commit your API keys or credentials to the repository
- Use environment variables for sensitive information
- Keep your reference data files secure

## Contributing

Feel free to submit issues and enhancement requests!

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
  pip install -r requirements.txt
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

### 3. Set Up Environment Variables

Set up your environment variables in your shell profile (e.g., `~/.zshrc` or `~/.bashrc`):
```bash
# Perplexity API
export PERPLEXITY_API_KEY='your-api-key-here'

# Kaufmich credentials
export KAUFMICH_USERNAME='your-username'
export KAUFMICH_PASSWORD='your-password'
```

### 4. Collect Authentic Reviews

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

### 5. Collect Fake Reviews

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

### 6. Analyze a Profile in Question

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

## Notes

- The script handles pagination by scrolling to load additional reviews
- Star ratings are extracted from the reviewer's rating section
- All data is saved with timestamps and full review content
- Login is required to access most profiles' reviews

## Troubleshooting

- If you encounter ChromeDriver errors, make sure your Chrome browser version matches your ChromeDriver version
- If you get security warnings on macOS, run the command in step 2 to remove quarantine attributes
- For login issues, verify your credentials and check if the site's login process has changed
- If you get credential errors, make sure your environment variables are set correctly

## Additional Tips

- **Data Structure**: Each review contains profile name, reviewer link, date, content and star count
- **Recovery**: If script crashes, restart with fewer profiles at once
- **Rate Limiting**: Add delays between profiles to avoid IP blocks
- **Captchas**: If captchas appear, slow down scraping or use a different IP
- **Analysis Patterns**: Look for similar reviewers, identical text, unusual timing
- **Large Profiles**: Profiles with many reviews may take several minutes to scrape
- **Legal Note**: Use responsibly and in accordance with site terms of service 
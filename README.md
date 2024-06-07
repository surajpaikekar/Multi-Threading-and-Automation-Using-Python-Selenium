# Multi-Threading and Web Automation Using Python-Selenium

## Overview

This repository provides a sample codebase for automating web interactions and performing web scraping using Python, Selenium, and threading. It demonstrates advanced techniques such as parallel processing for efficient data extraction from multiple URLs simultaneously.

## Getting Started

### Prerequisites

- Python installed on your system.
- Selenium WebDriver installed (`pip install selenium`).

### Steps to Follow

#### Step 1: Download and Extract Code

Download the provided codebase from the link below and extract its contents.

#### Step 2: Analyze the Functions

Focus on understanding the `main_parallel` and `main` functions, as they contain the core logic for parallel web scraping.

### Step 3: Update XPaths

Adjust the XPaths in the script to match the current structure of the target website's login form.

#### Note

The code assumes the existence of a separate `login.py` file, which is imported to obtain the latest WebDriver instance. This WebDriver is then utilized throughout the codebase for automation purposes.

### Understanding the Workflow

1. **URLs Creation**: The `urls_creation` function generates a list named `ndis_urls_response_list`, which contains 10 sub-lists (`ndis_urls_response_list1` to `ndis_urls_response_list10`). Each sub-list holds URLs for scraping.

2. **Driver Creation**: The `driver_creation` function creates a corresponding list of 10 WebDriver instances, one for each sub-list of URLs. These drivers are allocated for parallel processing of the scraping tasks.

3. **Main Parallel Execution**: The `main_parallel` function orchestrates the scraping process:
   - It calls the `main` function, which in turn invokes the `parse_table` function.
   - `parse_table` navigates to a single URL using a single WebDriver instance and calls the `get_details` function to scrape data.
   - `get_details` returns the scraped data as a list, which is passed back to `parse_table`.
   - Finally, `main` receives this data, processes it into a DataFrame, identifies any failed URLs, and prepares the results for storage.

4. **Final Results Collection**: The `main_parallel` function collects the processed DataFrames and failed URLs in the `wait` function, preparing them for local storage.

### Running the Code

This is just demonstration to show how Parallel Processing works using Python-Selenium:



**Note**: This guide assumes the existence of a separate `login.py` file, which is imported to obtain the latest WebDriver instance. This WebDriver is then utilized throughout the codebase for automation purposes.

## Additional Information

- Ensure your Selenium WebDriver is compatible with the version of the browser you intend to use.
- Running the script in headless mode is possible but requires additional setup for capturing screenshots or logs.

## Troubleshooting

If you encounter issues during execution, check the following:

- Verify all credentials and URLs are correctly entered.
- Confirm the XPaths match the current layout of the target website.
- Ensure your Selenium WebDriver is up-to-date and matches your browser version.

## Conclusion

By following these steps, you should be able to successfully automate the Multi-Threading approach using Python and Selenium. Remember, this approach relies heavily on the current state of the target website, so minor changes to the site's layout may require adjustments to the script.



"""

Scenario : - We need to fetch th details of participant available on the webpage.

Process - 
- Logging into the website with 2FA
- Automate to the webpage where list of participants along with their Unique corresponding number is available 
- On the participant webpage there are button such as - First, Last, 5, 10, 20, 50.
- First and Last buttons represent the first and Last page respectively.
- 5, 10, 20, 50 buttons represent the number of participants will be displayed on single page.
- For instance if click on button 50 then 50 partipants along with their Unique corresponding numbers will displayed.
- Automate the script using selenium to scrape Unique Numbers from the partcipant page [ using Pagination]
- Now suppose we found almost 2000 Unique Numbers corresponding to each participant
- Divide these Numbers into 10 LISTs for parallel processing [Each having 200]
- Create 10 separate web driver instance for each list to scrape data from each participant separately
- Pass these 10 drivers along with 10 LISTs in the main_parallel function
- This will introduce Multi Threading - Each Driver will be used for each LIST as a thread
- Using single driver working for 200 participants, this single driver can automate through each parcipants[out of 200] page to scrape the details
- On the each participants page [after getting into using their Unique Numbers] we will see following things- 
            - Name
            - Unique Number 
            - Duration

- Automate the selenium script to scrape the above tags and effectively.
- Click on the budget button and scrape the table data
- clcik on the provider_role button and scrape the table data

- Store data in CSV file 



"""


import time
from datetime import date, timedelta, datetime
from lxml import etree, html
from requests_futures.sessions import FuturesSession
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import sys
import imaplib
import base64
import email
import re
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, UnexpectedTagNameException
from tqdm.notebook import tqdm
import logging
from pathlib import Path
from  concurrent.futures import ThreadPoolExecutor, wait
from tqdm import tqdm
logging.basicConfig(filename='budget_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

## importing the Login module locally
from login.login import get_chrome_driver, proda_login




driver  = get_chrome_driver()
driver.set_window_size(1200, 800) 
driver  = proda_login(driver)
print(f"Main driver initialized: ")

#### output cookies, sessions and user agent #######
cookies_list =  driver.get_cookies()
selenium_user_agent = driver.execute_script("return navigator.userAgent;")
print(f"user agent: {selenium_user_agent}")


def drivers_creation(num_drivers=10):
    """
    This function creates multiple Selenium webdriver instances for parallel processing.
    
    Parameters:
    - num_drivers: Number of webdriver instances to create (default is 10)
    
    Returns:
    - drivers: List of Selenium webdriver instances

    pass these drivers into main_parallel function,
    """
    start = time.time()
    drivers = []

    for i in range(num_drivers):
        driver = get_chrome_driver()
        driver = proda_login(driver)
        drivers.append(driver)
        print(f"Driver {i+1} initialized.")
        logging.info(f"Driver {i+1} initialized.")

    end = time.time()
    print(f"Total time taken to create {num_drivers} drivers: {end - start} secs")
    logging.info(f"Total time taken to create {num_drivers} drivers: {end - start} secs")

    return drivers

drivers = drivers_creation

###################################################################################################################

def url_creation(numbers):
    """
        - Implment the function to create URLs according to website domain URL strcuture
        - return : ndis_urls_response_list-->> List of lists containing response codes
        - Pass this list into main_parallel
    """
ndis_urls_response_lists = url_creation()

#####################################################################################################################


def get_details(driver, url_response):

    """
        Implement the get_details() function for actual scraping here
        return : --> LIST

    """
    pass

#####################################################################################################################




def parse_tables(driver, url_response):
    """
    This function parses tables on the participant's budget page to extract budget details.
    
    Parameters:
    - driver: Selenium webdriver instance
    - url_response: Response object containing the URL and its response
    
    Returns:
    - details_df: DataFrame containing extracted budget details
    - failed_urls: List of URLs for which extraction failed
    """
    failed_urls = []
    details_df = pd.DataFrame()
    try:
        logging.info(f"Processing URL: {url_response.url}")
       
        driver.get(url_response.url)
        
        # time.sleep(5)
        logging.info("Page loaded successfully.")
        # await asyncio.sleep(5)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(span, 'Budget')]"))
            )
            budget_button = driver.find_element(By.XPATH, "//button[contains(span, 'Budget')]")
            budget_button.click()

            ## extracting the details here
            details = get_details(driver, url_response)
            details_df = pd.DataFrame(details)
            logging.info(f"Length of details_df from get_details() of: {url_response.url}: {len(details_df)}")
            logging.info(f"Details extracted successfully for {url_response.url}")

        except TimeoutException as te:
            logging.error(f"Timeout waiting for element on {url_response.url}: {te}")
            details_df = pd.DataFrame() 
            failed_urls.append(url_response.url)

            
        except NoSuchElementException as nse:
            logging.warning(f"Budget button not found for {url_response.url}: {nse}")
            details_df = pd.DataFrame() 
            failed_urls.append(url_response.url)

            
        except Exception as e:
            logging.error(f"Error in reading tables for {url_response.url}: {e}")
            details_df = pd.DataFrame() 
            failed_urls.append(url_response.url)
            driver.save_screenshot(f"screenshot_{url_response.url}.png")


    except Exception as e:
        logging.error(f"Unexpected error processing URL in driver: {url_response.url}: {e}")
        logging.error(f"Timeout waiting for My Participants page: {e}") 
        details_df = pd.DataFrame() 
        failed_urls.append(url_response.url)

        

    return details_df, failed_urls


def main(driver, ndis_urls_response_list):
    """
    This function orchestrates the main extraction process for a list of NDIS URLs.
    
    Parameters:
    - driver: Selenium webdriver instance
    - ndis_urls_response_list: List of NDIS URLs
    
    Returns:
    - final_details_df: DataFrame containing all extracted budget details
    - failed_urls: List of URLs for which extraction failed
    """
    final_details_df = pd.DataFrame()
    failed_urls = []

    start = time.time()
    
    try:
        ndis_urls_copy = ndis_urls_response_list.copy()
        results = [parse_tables(driver, response) for response in ndis_urls_copy]
        # results = [parse_tables(driver, response) for response in tqdm(ndis_urls_copy, total=len(ndis_urls_copy), desc="Processing total URLs")]

        data_frames = [result[0] for result in results if result is not None]
        failed_urls = [url for result in results if result is not None for url in result[1]]

        if data_frames:
            final_details_df = pd.concat(data_frames, ignore_index=True)
            final_details_df.drop_duplicates(inplace=True)

            """
                cleaning the data frame : Replacing the "Exhausted" text with 0 and '−' with  '-' [hyphen]
            """

            columns_to_clean = ["Allocated", "Spent", "Available Balance"]
            final_details_df[columns_to_clean] = final_details_df[columns_to_clean].replace("Exhausted", 0)
            final_details_df[columns_to_clean] = final_details_df[columns_to_clean].apply(lambda x: x.str.replace('−', '-'))
        else:
            logging.warning("No results retrieved from the tasks.")
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        # sys.exit(1)

    end = time.time()
    print(f"Total time taken to Extract One LIST: {end - start} secs")
    logging.info(f"Total time taken to Extract One LIST: {end - start} secs")
    print(f"length of data frame for One LIST: {len(final_details_df)}")
    logging.info(f"length of data frame for One LIST: {len(final_details_df)}")
    return final_details_df, failed_urls
    
# ########################################## using ThreadPoolExecutor ##############################


"""
        This is the main Multi Threading Function here

"""


def main_parallel(drivers, ndis_urls_response_lists):
    """
    This function orchestrates parallel processing of budget extraction for multiple drivers and NDIS URL lists.
    
    Parameters:
    - drivers: List of Selenium webdriver instances
    - ndis_urls_response_lists: List of lists containing NDIS URLs for parallel processing
    
    Returns:
    - final_details_df: DataFrame containing all extracted budget details
    - failed_urls: List of URLs for which extraction failed
    """
    ndis_lists = {}
    driver_dict = {}

    # Unpack each list from ndis_urls_response_lists and store them with the same name
    for i, sublist in enumerate(ndis_urls_response_lists, start=1):
        ndis_lists[f"ndis_urls_response_list{i}"] = sublist 

    # Unpack each driver from the drivers list and store them with the same name
    for i, driver in enumerate(drivers, start=1):
        driver_dict[f"driver{i}"] = driver

    print('Extraction begins: ')
    logging.info('Extraction begins: ')
    start = time.time()  
    with ThreadPoolExecutor(max_workers=28) as executor:
        futures = []
        for i, driver in enumerate(drivers, start=1):
            sublist = ndis_lists.get(f"ndis_urls_response_list{i}")
            futures.append(executor.submit(main, driver, sublist))

        """
            Collecting all the results in 'wait function'
        """

        wait(futures)

        final_details_dfs = []
        failed_urls = []
        for i, future in enumerate(futures, start=1):
            final_details_df, failed = future.result()

            final_details_dfs.append(final_details_df)
            failed_urls.extend(failed)

    final_details_df = pd.concat(final_details_dfs, ignore_index=True)
    print(f"Length of final_details_df: {len(final_details_df)}")
    logging.info(f"Length of final_details_df: {len(final_details_df)}")
    print(f"Failed URLs length: {len(failed_urls)}")
    logging.info(f"Failed URLs length: {len(failed_urls)}")
    print("Extraction of Ends:")
    logging.info("Extraction of Ends:")
    end = time.time()
    print(f"Total time taken to extract all LISTs: {end - start}")
    logging.info(f"Total time taken to extract all LISTs: {end - start}")

    return final_details_df, failed_urls


final_details_df, failed_urls = main_parallel(drivers, ndis_urls_response_lists)


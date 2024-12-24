import os
import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Set up logging
logging.basicConfig(filename='wifi_login.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Script started')

def check_connection():
    logging.info('Checking connection status...')
    try:
        # Ping Google DNS
        response = requests.get("https://8.8.8.8", timeout=5)
        logging.info(f"Connection status: {response.status_code}")
        return True
    except requests.ConnectionError:
        logging.info("Connection error.")
        return False

def login_to_wifi():
    # Path to your ChromeDriver
    chrome_driver_path = "./chromedriver.exe"
    
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    
    # Initialize browser with the new Service object
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Get the login URL from environment variables
    login_URL = os.getenv("LOGIN_URL")
    logging.info("Retrieved URL:", login_URL)

    # Open the Wi-Fi login page
    driver.get(str(login_URL))
    
    # Get credentials from environment variables
    username_input = os.getenv("WIFI_USERNAME")
    password_input = os.getenv("WIFI_PASSWORD")
    
    if not username_input or not password_input:
        logging.info("Wi-Fi credentials not set.")
        return
    
    retry_attempts = 10
    for attempt in range(retry_attempts):
        try:
            logging.info(f"Attempt {attempt + 1} to connect...")

            # Fill in the login form
            username = driver.find_element(By.ID, "cred_userid_inputtext")
            password = driver.find_element(By.ID, "cred_password_inputtext")
            username.send_keys(username_input)
            password.send_keys(password_input)

            # Submit the form
            login_button = driver.find_element(By.ID, "cred_sign_in_button")
            login_button.click()
            logging.info("Logged in successfully.")
            driver.quit()
            return  # Exit the function if login is successful

        except WebDriverException as e:
            logging.info(f"Failed to connect: {e}")
            driver.quit()
            time_to_wait = 2 ** attempt  # Exponential backoff: 2, 4, 8, etc.
            logging.info(f"Retrying in {time_to_wait} seconds...")
            time.sleep(time_to_wait)

    logging.info("Failed to connect after several attempts.")

def main():
    time.sleep(60)  # Wait for the network to initialize
    while True:
        logging.info(time.strftime("%H:%M:%S", time.localtime()) + " => ")
        if not check_connection():
            logging.info("No connection detected, attempting to log in...")
            login_to_wifi()
        else:
            logging.info("Wi-Fi is connected.")
        
        time.sleep(600)  # Check connection every 10 minutes

        if time.localtime().tm_hour == 7:
            # clear the log file at 7 AM
            open('wifi_login.log', 'w').close()
            logging.info('Log file cleared at 7 AM')

if __name__ == "__main__":
    main()

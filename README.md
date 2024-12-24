# WiFi AutoLogin Script

This script automatically detects your WiFi connection status and logs into the network if disconnected. It's designed to handle intermittent network disconnections in environments with poor internet connections.

## Features
- Checks internet connectivity periodically.
- Automatically logs into a predefined WiFi network using stored credentials.
- Runs silently in the background (headless browser mode).
- Exponential backoff for retrying failed login attempts.
- Clears the log file daily at 7 AM to manage log size.

---

## Requirements
1. **Python 3.x**: Ensure Python is installed and available in your system's PATH.
2. **Dependencies**: Install the required Python packages using:
   ```bash
   pip install selenium requests
   ```
3. **ChromeDriver**: Download the version of ChromeDriver compatible with your installed version of Google Chrome. Place it in the project directory or add it to your system's PATH.
   - Download ChromeDriver: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
4. **Google Chrome**: Ensure the Google Chrome browser is installed and updated.

---

## Setup

1. **Environment Variables**: Set the following environment variables:
   - `LOGIN_URL`: The URL of your WiFi login page.
   - `WIFI_USERNAME`: Your WiFi username.
   - `WIFI_PASSWORD`: Your WiFi password.

   On Linux/macOS, you can add these to your `.bashrc` or `.zshrc`:
   ```bash
   export LOGIN_URL="http://example.com/login"
   export WIFI_USERNAME="your_username"
   export WIFI_PASSWORD="your_password"
   ```
   On Windows, set them via the Environment Variables settings.

2. **ChromeDriver Path**: If you place `chromedriver.exe` in a custom location, update the `chrome_driver_path` variable in the script to the correct path.

---

## Usage

1. Run the script:
   ```bash
   python wifi_autologin.py
   ```

2. The script will:
   - Check your internet connection every 10 minutes.
   - Attempt to log in to the network if disconnected.
   - Write logs to `wifi_login.log` for monitoring activity.

---

## Logging
- The script maintains a log file (`wifi_login.log`) with timestamps and statuses of connection checks and login attempts.
- The log file is automatically cleared daily at 7 AM to prevent bloating.

---

## Running the Script on Windows Startup
To ensure the script runs automatically when Windows starts, you can add it to Windows Task Scheduler. Configure a task to execute the script or a .bat file pointing to the script on startup, ensuring uninterrupted internet connectivity for remote usage.

---

## Troubleshooting
- **Connection Error**: If the script cannot connect to the internet, check your `LOGIN_URL`, `WIFI_USERNAME`, and `WIFI_PASSWORD` environment variables.
- **ChromeDriver Issues**: Ensure ChromeDriver matches your Chrome browser version. If there are compatibility errors, download the correct version from [here](https://chromedriver.chromium.org/downloads).
- **Timeout Issues**: Increase the `timeout` value in the `requests.get` call within the `check_connection` function if necessary.

---
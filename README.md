# Twitter Automation CLI (Playwright)

A command-line application designed to automate certain Twitter interactions using browser automation with Playwright. It aims to allow users to log in, collect tweets, and (in future versions) analyze and post content.

## Current Features

*   Command-Line Interface (CLI).
*   Secure credential input for Twitter login (credentials stored in memory only during session).
*   Automated login to Twitter via Playwright.
*   Basic collection of tweets from the home timeline (author and text).
*   Configuration via a `.env` file for headless mode and wait times.
*   Basic logout capability.

## Limitations

*   **UI Dependency**: Highly dependent on Twitter's current website UI selectors; may break if Twitter updates its site.
*   **No 2FA**: Does not currently handle Two-Factor Authentication (2FA) during login.
*   **Basic Error Handling**: Error handling is currently basic.
*   **Incomplete Features**: Content analysis and content posting features are not yet implemented.
*   **CLI Only**: No Graphical User Interface (GUI).

## Setup Instructions

1.  **Prerequisites**: Ensure Python 3.7+ is installed on your system.
2.  **Clone Repository**: `git clone <repository_url>` (Replace `<repository_url>` with the actual URL of this repository).
3.  **Navigate to Directory**: `cd <project_directory>` (Replace `<project_directory>` with the name of the cloned folder).
4.  **Create & Activate Virtual Environment** (Recommended):
    *   `python -m venv venv`
    *   Windows: `venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`
5.  **Install Dependencies**: `pip install -r requirements.txt`
6.  **Install Playwright Browsers**: `playwright install`
    *   This command downloads necessary browser binaries (e.g., Chromium) for Playwright to use.
7.  **Configure Environment**: Create a `.env` file in the root of the project directory. You can copy the example below:
    ```env
    # Twitter Automation Configuration
    # Set to true or false (e.g., true for no browser UI, false to watch it operate)
    HEADLESS_MODE=true
    # Default wait time in milliseconds for browser actions (e.g., 5000 for 5 seconds)
    DEFAULT_WAIT_TIME=5000
    ```

## Usage Instructions

All commands are run via the main script from the root project directory. Ensure your virtual environment is activated.

*   **View Help**: To see all available commands and options:
    `python -m src.main --help`
*   **Log In**:
    `python -m src.main login`
    You will be prompted for your Twitter username (or email/phone) and password.
*   **Collect Tweets**:
    `python -m src.main collect --scrolls N`
    (Replace `N` with the number of times you want to scroll down the timeline, e.g., `2`). This command requires you to be logged in first.
*   **Check Status**: To see the current configuration and login status:
    `python -m src.main status`
*   **Log Out**:
    `python -m src.main logout`

## Security Note

This application will ask for your Twitter credentials. These are used solely for the purpose of logging into Twitter via browser automation and are **only stored in memory** during the application's active session. They are not written to disk or any other persistent storage by this application.

Be mindful of the security of the machine where you run this tool. Ensure your system is secure to protect any sensitive information, including your Twitter credentials, while the application is running.

import click
import getpass
from playwright.sync_api import sync_playwright, BrowserContext, Page
from src.config import app_config # Assuming app_config.HEADLESS_MODE and app_config.DEFAULT_WAIT_TIME exist

# Store browser_context and page globally within the module for now
# This is a simplification for the initial CLI version.
# A more robust solution would involve a class or better state management.
_browser_context: BrowserContext = None
_page: Page = None
_playwright_instance = None


def login_to_twitter() -> Page:
    """
    Handles the Twitter login process using Playwright.
    Prompts user for username and password.
    Navigates to Twitter, fills in credentials, and attempts to log in.
    Returns the authenticated Page object or None on failure.
    """
    global _browser_context, _page, _playwright_instance

    if _page:
        click.echo("Already logged in.")
        # Check if still on a valid Twitter page (e.g., home timeline)
        if "twitter.com/home" in _page.url:
             return _page
        else:
            click.echo("Session might be invalid, attempting relogin flow.")
            # Fall through to login logic

    username = click.prompt("Enter your Twitter username (or email/phone)")
    password = getpass.getpass("Enter your Twitter password: ")

    try:
        _playwright_instance = sync_playwright().start()
        browser = _playwright_instance.chromium.launch(headless=app_config.HEADLESS_MODE)
        _browser_context = browser.new_context()
        _page = _browser_context.new_page()

        click.echo("Navigating to Twitter login page...")
        _page.goto("https://twitter.com/login", timeout=app_config.DEFAULT_WAIT_TIME * 12) # 60s timeout for login page

        # Wait for the username input field to be visible
        username_input_selector = "input[name='text']" # Common selector for username/email/phone
        _page.wait_for_selector(username_input_selector, timeout=app_config.DEFAULT_WAIT_TIME * 4) # 20s
        _page.fill(username_input_selector, username)

        # Click "Next"
        # Twitter's login flow can vary. This selector targets a button with "Next" text.
        # It might need adjustment if the UI changes.
        _page.click("div[role='button']:has-text('Next')")


        # Twitter might ask for phone/username verification if login seems suspicious
        # This is a common intermediate step.
        # Looking for an input field that often has 'phone' or 'username' in its name attr or label
        # For now, we'll try to fill it with username again if it appears.
        phone_username_verification_selector = "input[name='text'][type='text']" # A bit generic, hoping it's the right one
        try:
            _page.wait_for_selector(phone_username_verification_selector, timeout=app_config.DEFAULT_WAIT_TIME * 2) # 10s
            # Check if the element is visible and enabled before filling
            if _page.is_visible(phone_username_verification_selector) and _page.is_enabled(phone_username_verification_selector):
                click.echo("Twitter is asking for phone/username verification. Filling with username again.")
                _page.fill(phone_username_verification_selector, username)
                _page.click("div[role='button']:has-text('Next')") # Click "Next" again
        except Exception:
            # This step is optional, so we pass if it's not found
            click.echo("Phone/username verification step not detected or timed out. Proceeding...")


        password_input_selector = "input[name='password']"
        _page.wait_for_selector(password_input_selector, timeout=app_config.DEFAULT_WAIT_TIME * 2)
        _page.fill(password_input_selector, password)
        _page.click("div[role='button']:has-text('Log in')")

        # Wait for navigation to home timeline as an indication of successful login
        # or for an error message.
        _page.wait_for_url("https://twitter.com/home", timeout=app_config.DEFAULT_WAIT_TIME * 6) # 30s

        click.secho("Successfully logged in to Twitter!", fg="green")
        return _page

    except Exception as e:
        click.secho(f"Login failed: {e}", fg="red")
        if _playwright_instance:
            _playwright_instance.stop() # Stop playwright if an error occurs
        _playwright_instance = None
        _browser_context = None
        _page = None
        return None


def logout_from_twitter():
    """
    Logs out from Twitter by closing the browser context and stopping Playwright.
    """
    global _browser_context, _page, _playwright_instance
    if _browser_context:
        _browser_context.close()
        _browser_context = None
        click.echo("Browser context closed.")
    if _playwright_instance:
        _playwright_instance.stop()
        _playwright_instance = None
        click.echo("Playwright stopped.")

    _page = None # Clear the page object
    click.echo("Logged out and session data cleared from memory.")

if __name__ == '__main__':
    # Test functions
    page = login_to_twitter()
    if page:
        print(f"Current URL after login: {page.url}")
        print("Login successful. Try to navigate to home.")
        page.goto("https://twitter.com/home")
        print(f"Current URL: {page.url}")
        page.wait_for_timeout(5000) # Wait 5 seconds to observe

    logout_from_twitter()

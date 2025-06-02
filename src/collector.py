import click
from playwright.sync_api import Page
from src.auth import _page as authenticated_page # Accessing the global page object from auth
from src.config import app_config
import time

def fetch_home_timeline_tweets(num_scrolls: int = 2) -> list[dict]:
    """
    Fetches tweets from the user's home timeline.

    Args:
        num_scrolls: Number of times to scroll down to load more tweets.

    Returns:
        A list of dictionaries, where each dictionary contains 'author' and 'text'.
        Returns an empty list if not logged in or if an error occurs.
    """
    if not authenticated_page or "twitter.com/home" not in authenticated_page.url:
        click.secho("You must be logged in and on the home timeline to fetch tweets.", fg="red")
        click.echo("Please try logging in first. Current page: {}".format(authenticated_page.url if authenticated_page else 'N/A'))
        return []

    page = authenticated_page
    collected_tweets = []

    try:
        click.echo("Navigating to home timeline (if not already there)...")
        if "twitter.com/home" not in page.url: # Ensure we are on the home page
             page.goto("https://twitter.com/home", timeout=app_config.DEFAULT_WAIT_TIME * 2)
             page.wait_for_url("https://twitter.com/home", timeout=app_config.DEFAULT_WAIT_TIME * 2)


        click.echo(f"Scrolling {num_scrolls} times to load tweets...")
        for i in range(num_scrolls):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(app_config.DEFAULT_WAIT_TIME / 2000) # Wait for content to load after scroll (e.g. 2.5s if default is 5000ms)
            click.echo(f"Scroll {i+1}/{num_scrolls} complete.")

        # Selector for individual tweets (Twitter uses <article> tags)
        # This selector might need frequent updates.
        tweet_selector = "article div[data-testid='tweetText']"
        author_selector_relative_to_article = "div[data-testid='User-Name'] span:has-text('@')"


        tweet_elements = page.query_selector_all("article[data-testid='tweet']")
        click.echo(f"Found {len(tweet_elements)} potential tweet articles.")

        if not tweet_elements:
            click.secho("No tweet articles found. The page structure might have changed or no tweets loaded.", fg="yellow")
            return []

        for tweet_article in tweet_elements:
            try:
                tweet_text_element = tweet_article.query_selector("div[data-testid='tweetText']")
                user_name_element = tweet_article.query_selector("div[data-testid='User-Name']") # This often has display name and @handle

                tweet_text = tweet_text_element.inner_text() if tweet_text_element else "N/A"

                author_handle = "N/A"
                if user_name_element:
                    # Try to find the @handle within the user name element
                    handle_elements = user_name_element.query_selector_all("span")
                    for span in handle_elements:
                        text_content = span.inner_text()
                        if text_content and text_content.startswith("@"):
                            author_handle = text_content
                            break
                    if author_handle == "N/A": # Fallback if specific span not found
                        author_handle = user_name_element.inner_text().splitlines()[-1] # Often the last line after display name

                if tweet_text != "N/A": # Only add if we found text
                    collected_tweets.append({"author": author_handle.strip(), "text": tweet_text.strip()})
            except Exception as e:
                click.echo(f"Error processing a tweet: {e}", fg="yellow")
                continue # Skip this tweet if there's an error

        click.secho(f"Successfully collected {len(collected_tweets)} tweets.", fg="green")
        return collected_tweets

    except Exception as e:
        click.secho(f"Error fetching tweets: {e}", fg="red")
        return []

if __name__ == '__main__':
    # This part is for direct testing of the collector.
    # It requires the user to be already logged in via running auth.py or similar.
    # For this subtask, we will not run this directly, but it's good for future manual testing.
    if not authenticated_page:
        click.secho("Please log in first by running the main CLI login command.", fg="red")
    else:
        click.echo(f"Attempting to fetch tweets using page: {authenticated_page.url}")
        tweets = fetch_home_timeline_tweets(num_scrolls=1)
        if tweets:
            for i, tweet in enumerate(tweets):
                print(f"--- Tweet {i+1} ---")
                print(f"Author: {tweet['author']}")
                print(f"Text: {tweet['text']}")
        else:
            print("No tweets collected or an error occurred.")

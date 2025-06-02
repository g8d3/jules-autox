import click
from src.config import app_config
from src.auth import login_to_twitter, logout_from_twitter, _page as authenticated_page # Import _page
from src.collector import fetch_home_timeline_tweets # New import

@click.group()
def cli():
    """Twitter Automation App CLI"""
    pass

@cli.command()
def login():
    """Log in to Twitter."""
    click.echo("Attempting to log in...")
    page = login_to_twitter()
    if page:
        click.echo(f"Login successful. Current page: {page.url}")
    else:
        click.echo("Login failed. Please check credentials or console output.")

@cli.command()
def logout():
    """Log out from Twitter and clear session."""
    logout_from_twitter()

@cli.command()
@click.option('--scrolls', default=2, help='Number of times to scroll down the timeline.')
def collect(scrolls: int):
    """Fetch tweets from your home timeline."""
    if not authenticated_page or "twitter.com/home" not in authenticated_page.url:
        click.secho("You need to be logged in to collect tweets. Please run 'login' first.", fg="red")
        return

    click.echo(f"Collecting tweets with {scrolls} scroll(s)...")
    tweets = fetch_home_timeline_tweets(num_scrolls=scrolls)
    if tweets:
        click.secho(f"Collected {len(tweets)} tweets:", fg="green")
        for i, tweet in enumerate(tweets):
            click.echo(f"--- Tweet {i+1} ---")
            click.echo(f"Author: {tweet['author']}")
            click.echo(f"Text: {tweet['text']}")
    else:
        click.secho("No tweets collected or an error occurred.", fg="yellow")

@cli.command()
def status():
    """Show current configuration and login status."""
    click.echo(f"Headless Mode: {app_config.HEADLESS_MODE}")
    click.echo(f"Default Wait Time (ms): {app_config.DEFAULT_WAIT_TIME}")
    if authenticated_page:
        click.echo(f"Login Status: Logged in (Page URL: {authenticated_page.url})")
    else:
        click.echo("Login Status: Not logged in")


if __name__ == '__main__':
    cli()

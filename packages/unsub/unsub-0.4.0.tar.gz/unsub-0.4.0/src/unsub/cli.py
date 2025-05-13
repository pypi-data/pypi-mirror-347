import click
import datetime
import os
import tomli
import tomli_w
from pathlib import Path
from unsub.applets import Downloader, Analzyer, Reviewer
from unsub.storage import DataStore
from unsub.email import IMAPClient


class DateParamType(click.ParamType):
    name = "date"

    def convert(self, value, param, ctx):
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            self.fail(f"{value!r} is not a valid date in YYYY-MM-DD format", param, ctx)


@click.group()
@click.option(
    "--imap-server",
    help="IMAP server address (can also use UNSUB_IMAP_SERVER env var or config file)",
)
@click.option(
    "--email", help="Email account (can also use UNSUB_EMAIL env var or config file)"
)
@click.option(
    "--password",
    help="Email password (can also use UNSUB_PASSWORD env var or config file)",
)
@click.option("--db-path", default="emails.db", help="Path to SQLite database")
@click.pass_context
def cli(ctx, imap_server, email, password, db_path):
    """Unsub - Email management and unsubscribe automation tool."""
    # Check config file first
    config_file = Path.home() / ".config" / "unsub" / "config.toml"
    config_data = {}
    if config_file.exists():
        with open(config_file, "rb") as f:
            config_data = tomli.load(f)

    # Check environment variables if command line options aren't provided
    imap_server = (
        imap_server
        or os.environ.get("UNSUB_IMAP_SERVER")
        or config_data.get("imap_server", "imap.gmail.com")
    )
    email = email or os.environ.get("UNSUB_EMAIL") or config_data.get("email")
    password = (
        password or os.environ.get("UNSUB_PASSWORD") or config_data.get("password")
    )

    if not email:
        raise click.UsageError(
            "Email must be provided either via --email, UNSUB_EMAIL environment variable, or config file"
        )
    if not password:
        raise click.UsageError(
            "Password must be provided either via --password, UNSUB_PASSWORD environment variable, or config file"
        )

    ctx.ensure_object(dict)
    ctx.obj["IMAP_SERVER"] = imap_server
    ctx.obj["EMAIL"] = email
    ctx.obj["PASSWORD"] = password
    ctx.obj["DB_PATH"] = db_path


@cli.command()
@click.option(
    "--days",
    type=int,
    default=30,
    help="Number of days to check emails for",
)
@click.pass_context
def check(ctx, days):
    """Check email count from past n days."""
    with IMAPClient(
        ctx.obj["IMAP_SERVER"], ctx.obj["EMAIL"], ctx.obj["PASSWORD"]
    ) as client:
        click.echo(f"\n📊 Email Count for Past {days} Days")
        click.echo("=" * 40)

        counts = client.count_emails_past_days(days)
        total = 0
        for date, count in counts.items():
            click.echo(f"{date.strftime('%Y-%m-%d')}: {count:4d} emails")
            total += count

        click.echo("=" * 40)
        click.echo(f"Total: {total:4d} emails")


@cli.command()
@click.argument(
    "date",
    type=DateParamType(),
    required=False,
)
@click.pass_context
def download(ctx, date):
    """Download emails from a specific day.

    DATE: Specific date to download emails from (YYYY-MM-DD format). If not provided, uses today's date.
    """
    db = DataStore(ctx.obj["DB_PATH"])
    with IMAPClient(
        ctx.obj["IMAP_SERVER"], ctx.obj["EMAIL"], ctx.obj["PASSWORD"]
    ) as client:
        db.clear_database()
        downloader = Downloader(client, db)
        target_date = date or datetime.date.today()
        downloader.download_one_day(target_date)


@cli.command()
@click.pass_context
def analyze(ctx):
    """Analyze downloaded emails."""
    db = DataStore(ctx.obj["DB_PATH"])
    analyzer = Analzyer(db)
    analyzer.analyze_all()


@cli.command()
@click.pass_context
def review(ctx):
    """Review analyzed emails."""
    db = DataStore(ctx.obj["DB_PATH"])
    with IMAPClient(
        ctx.obj["IMAP_SERVER"], ctx.obj["EMAIL"], ctx.obj["PASSWORD"]
    ) as client:
        reviewer = Reviewer(db, client)
        reviewer.review_all()


@cli.command()
def config():
    """Configure unsub with default settings."""
    config_dir = Path.home() / ".config" / "unsub"
    config_file = config_dir / "config.toml"

    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load existing config if it exists
    config_data = {}
    if config_file.exists():
        with open(config_file, "rb") as f:
            config_data = tomli.load(f)

    click.echo("\n🔧 Unsub Configuration Wizard")
    click.echo("=" * 40)

    # Email configuration
    click.echo("\n📧 Email Configuration")
    click.echo("-" * 40)

    email = click.prompt(
        "Email address", default=config_data.get("email", ""), show_default=True
    )

    click.echo("\n🔐 Password Configuration")
    click.echo("-" * 40)
    click.echo("For Gmail users: You'll need to create an App Password")
    click.echo("1. Visit: https://myaccount.google.com/apppasswords")
    click.echo("2. For App name enter 'unsub'")
    click.echo("3. Click create")
    click.echo("4. Copy the generated password and paste it below")
    click.echo("\nFor other email providers: Use your regular password")

    password = click.prompt(
        "Password",
        default=config_data.get("password", ""),
        hide_input=True,
        show_default=False,
    )

    # IMAP server configuration
    click.echo("\n📡 IMAP Server Configuration")
    click.echo("-" * 40)
    click.echo("Default is imap.gmail.com for Gmail users")

    imap_server = click.prompt(
        "IMAP server",
        default=config_data.get("imap_server", "imap.gmail.com"),
        show_default=True,
    )

    # Save configuration
    config_data = {"email": email, "password": password, "imap_server": imap_server}

    with open(config_file, "wb") as f:
        tomli_w.dump(config_data, f)

    click.echo(f"\n✅ Configuration saved to {config_file}")
    click.echo("\nYou can now use unsub without specifying email and password options.")
    click.echo(
        "The configuration will be used as defaults when running unsub commands."
    )


def main():
    """Entry point for the unsub command."""
    cli(obj={})


if __name__ == "__main__":
    main()

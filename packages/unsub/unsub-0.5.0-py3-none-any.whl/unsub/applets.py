import dataclasses
import datetime
import sys
import termios
import textwrap
import time
import tty
import webbrowser

import marvin
import pydantic_ai
from unsub.email import IMAPClient
from unsub.models import MessageModel, UnsubscribeModel
from unsub.storage import DataStore


class Downloader:
    def __init__(self, client: IMAPClient, db: DataStore) -> None:
        self.client = client
        self.db = db

    def download_one_day(self, date: datetime.date) -> int:
        print("\n" + "=" * 80)
        print(f"📅 Downloading emails for {date.strftime('%B %d, %Y')}")
        print("=" * 80 + "\n")

        imap_email_ids = self.client.imap_email_ids_on_date(date)
        print(f"📧 Found {len(imap_email_ids)} emails to process\n")

        for idx, imap_email_id in enumerate(imap_email_ids, 1):
            msg = self.client.fetch_email(imap_email_id)
            print(f"⏳ Downloading email {idx}/{len(imap_email_ids)}")
            print(f"   Subject: {msg.subject()}")
            print(f"   From: {msg.from_()}")
            print()

            if msg is not None:
                if self.db.message_hash_exists(msg.hash()):
                    print("✔️ Email already downloaded\n")
                    continue

                self.db.write(msg)
                print("✅ Email downloaded successfully\n")
            else:
                print("❌ Failed to process email\n")

    def download_all_days(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> None:
        """Download emails for a range of dates.

        Args:
            start_date: The first date to process
            end_date: The last date to process
        """
        current_date = start_date
        step = (
            datetime.timedelta(days=1)
            if start_date <= end_date
            else datetime.timedelta(days=-1)
        )

        while (step.days > 0 and current_date <= end_date) or (
            step.days < 0 and current_date >= end_date
        ):
            self.download_one_day(current_date)
            current_date += step


class Analyzer:
    @dataclasses.dataclass
    class _EmailAnalysis:
        summary: str
        unsubscribe_link: str | None
        unsubscribe_score_from_0_to_100_higher_supports_unsubscribing: int
        recommend_unsubscribe: bool

    def __init__(self, db: DataStore) -> None:
        self.db = db

    #     self.initialize_agent()

    # def initialize_agent(self):
    #     from pydantic_ai import Agent
    #     from pydantic_ai.models.openai import OpenAIModel
    #     from pydantic_ai.providers.openai import OpenAIProvider

    #     ollama_model = OpenAIModel(
    #         model_name="llama3.2",
    #         provider=OpenAIProvider(base_url="http://localhost:11434/v1"),
    #     )

    #     self.agent = Agent(ollama_model, output_type=self._EmailAnalysis)

    def analyze_email(self, email: MessageModel):
        content = f"""
Date: {email.received_at}
From: {email.sender}
Subject: {email.subject}
{'-' * 80}
{email.body}
        """

        instructions = f"""
You are a spam email assistant who helps users reduce their inbox clutter 
by identifying emails that they can unsubscribe from. 

Analyze the following email:

{content}
        """

        task = marvin.Task(
            instructions=instructions,
            result_type=self._EmailAnalysis,
            agents=[marvin.Agent(name="Email Analyzer", model="openai:gpt-4.1-mini")],
        )
        analysis = task.run()

        return analysis

    def analyze_all(self):
        unanalyzed_emails = self.db.get_unanalyzed_emails()

        if not unanalyzed_emails:
            print("\n📭 No emails to analyze!")
            return

        print("\n" + "=" * 80)
        print("🔍 Starting Email Analysis")
        print("=" * 80 + "\n")

        for email in unanalyzed_emails:
            print("\n" + "-" * 80)
            print(f"📨 Analyzing: {email.subject}")
            print("-" * 80)

            analysis = self.analyze_email(email)
            score = (
                analysis.unsubscribe_score_from_0_to_100_higher_supports_unsubscribing
            )

            print("\n⚠️  Analysis Result:")
            print(f"   • Unsubscribe Score: {score}/100")
            print(f"   • Summary: {analysis.summary}")
            print(
                f"   • Recommended Action: {'Unsubscribe' if analysis.recommend_unsubscribe else 'Keep'}"
            )

            # Update the email with analysis results
            session = self.db.Session()
            try:
                email = session.query(MessageModel).get(email.id)
                if email:
                    email.summary = analysis.summary
                    email.unsubscribe_link = analysis.unsubscribe_link
                    email.unsubscribe_score = score
                    email.analyzed = True
                    email.recommend_unsubscribe = analysis.recommend_unsubscribe
                    session.commit()
                    print("\n✅ Email marked as analyzed in database")
            finally:
                session.close()

        print("\n" + "=" * 80)
        print("✨ Analysis Complete")
        print("=" * 80 + "\n")


def get_single_key():
    """Get a single keypress from the user without requiring Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class Reviewer:
    def __init__(self, db: DataStore, client: IMAPClient) -> None:
        self.db = db
        self.client = client

    def display_email_review_form(self, email: MessageModel) -> None:
        """Display email details to the user."""
        print("\n" + "=" * 80)
        print("📧 EMAIL DETAILS")
        print("=" * 80)

        # Header section with key information
        print("\n📌 HEADER")
        print("-" * 40)
        print(f"👤 From:    {email.sender}")
        print(f"📝 Subject: {email.subject}")
        print(f"🕒 Date:    {email.received_at}")
        print("-" * 40)

        # Summary section if available
        if email.summary:
            print("\n📋 SUMMARY")
            print("-" * 40)
            print(textwrap.fill(email.summary, width=100))
            print("-" * 40)

        # Analysis results with visual indicators
        print("\n🔍 ANALYSIS RESULTS")
        print("-" * 40)

        # Score with visual indicator
        if email.unsubscribe_score is not None:
            score = email.unsubscribe_score
            score_emoji = "🟢" if score < 30 else "🟡" if score < 70 else "🔴"
            print(f"{score_emoji} Unsubscribe Score: {score}/100")

        print("-" * 40)

        # Action menu
        print("\n🎯 ACTIONS")
        print("-" * 40)
        print("u - Unsubscribe")
        print("o - Open")
        print("n - Next")
        print("e - Exit")
        print("-" * 40)
        print("\nEnter your choice: ", end="")

    def handle_unsubscribe(self, message_model: MessageModel) -> None:
        """Handle unsubscribe flow."""
        if not message_model.unsubscribe_link:
            print("❌ No unsubscribe link found for this email")
            return

        print(f"\n🔗 Unsubscribe link: {message_model.unsubscribe_link}")
        webbrowser.open(message_model.unsubscribe_link)

        # Delete the email using its ID
        if message_model.imap_email_id and self.client.delete_email(
            message_model.imap_email_id.encode()
        ):
            print("🗑️  Email deleted from Gmail")
        else:
            print("⚠️  Could not delete email")

        self.db.record_unsubscribe(reviewed_message_model_id=message_model.id)

    def handle_open(self, email: MessageModel) -> None:
        """Handle opening the email in browser."""
        # URL encode the subject to handle special characters
        encoded_subject = email.subject.replace(" ", "+")
        gmail_url = f"https://mail.google.com/mail/u/0/#search/{encoded_subject}"
        webbrowser.open(gmail_url)
        print("✅ Opening email in browser...")

    def review_all(self) -> None:
        """Review all unreviewed emails."""
        session = self.db.Session()
        try:
            while True:
                # Get the next unreviewed email
                email = (
                    session.query(MessageModel)
                    .filter_by(
                        reviewed=False, analyzed=True, recommend_unsubscribe=True
                    )
                    .order_by(MessageModel.received_at.desc())
                    .first()
                )

                if not email:
                    print("\n📭 No unreviewed emails found! Sleeping for 10 seconds...")
                    time.sleep(10)
                    continue

                # Check if we've already unsubscribed from this sender
                already_unsubscribed = (
                    session.query(UnsubscribeModel)
                    .join(MessageModel, UnsubscribeModel.message_id == MessageModel.id)
                    .filter(MessageModel.sender == email.sender)
                    .first()
                ) is not None

                if already_unsubscribed:
                    print(
                        f"\n⏭️ Skipping email from {email.sender} - already unsubscribed"
                    )
                    self.db.mark_as_reviewed(email.id)
                    continue

                self.display_email_review_form(email)

                while True:
                    choice = get_single_key().lower()
                    if choice in ["u", "o", "n", "e"]:
                        break
                    print("\rInvalid choice. Please press u, o, n, or e: ", end="")

                if choice == "u":
                    self.handle_unsubscribe(email)
                elif choice == "o":
                    self.handle_open(email)
                elif choice == "n":
                    print("⏭️ Skipping to next email...")
                elif choice == "e":
                    print("\n👋 Exiting email review...")
                    return

                print("Marking email as reviewed...")
                self.db.mark_as_reviewed(email.id)

        finally:
            session.close()

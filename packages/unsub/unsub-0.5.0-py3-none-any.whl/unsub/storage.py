import sqlalchemy
from sqlalchemy.orm import sessionmaker

from unsub.email import MessageFacade
from unsub.models import Base, MessageModel, UnsubscribeModel


class DataStore:
    def __init__(self, db_path: str = "unsub.db") -> None:
        self.engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
        self.Session = sessionmaker(bind=self.engine)

        Base.metadata.create_all(self.engine)

    def write(self, msg: MessageFacade) -> None:
        """Write the email to the database."""
        session = self.Session()
        try:
            session.add(msg.to_model())
            session.commit()
        finally:
            session.close()

    def record_unsubscribe(self, reviewed_message_model_id: int):
        """Write the email to the database."""
        session = self.Session()
        try:
            session.add(UnsubscribeModel(message_id=reviewed_message_model_id))
            session.commit()
        finally:
            session.close()

    def message_hash_exists(self, hash_) -> bool:
        """Check if an email with the same hash already exists in the database."""
        session = self.Session()
        try:
            return (
                session.query(MessageModel).filter_by(email_hash=hash_).first()
                is not None
            )
        finally:
            session.close()

    def clear_database(self) -> None:
        """Clear all data from the database."""
        session = self.Session()
        try:
            session.query(MessageModel).delete()
            session.commit()
        finally:
            session.close()

    def get_unanalyzed_emails(self) -> list[MessageModel]:
        """Get all unanalyzed emails."""
        session = self.Session()
        try:
            return (
                session.query(MessageModel)
                .filter_by(analyzed=False)
                .order_by(MessageModel.received_at.desc())
                .all()
            )
        finally:
            session.close()

    def mark_as_reviewed(self, imap_email_id: int) -> None:
        """Mark an email as reviewed."""
        session = self.Session()
        try:
            email = session.query(MessageModel).get(imap_email_id)
            if email:
                email.reviewed = True
                session.commit()
        finally:
            session.close()

    def update_analysis(self, imap_email_id: int, analysis: dict) -> None:
        """Update email with analysis results."""
        session = self.Session()
        try:
            email = session.query(MessageModel).get(imap_email_id)
            if email:
                email.summary = analysis.get("summary")
                email.unsubscribe_link = analysis.get("unsubscribe_link")
                email.unsubscribe_score = analysis.get(
                    "unsubscribe_score_from_0_to_100_higher_supports_unsubscribing"
                )
                session.commit()
        finally:
            session.close()

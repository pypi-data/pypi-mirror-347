import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class MessageModel(Base):
    __tablename__ = "message"

    # Downloader fields
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    received_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    sender = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    subject = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    body = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    imap_email_id = sqlalchemy.Column(
        sqlalchemy.String(255), nullable=False
    )  # Store the IMAP email ID
    email_hash = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    # Analyzer fields
    summary = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    unsubscribe_link = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)
    unsubscribe_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    recommend_unsubscribe = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    analyzed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    # Reviewer fields
    reviewed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


class UnsubscribeModel(Base):
    __tablename__ = "unsubscribe"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    message_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("message.id"), nullable=False
    )
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=False, default=func.now()
    )

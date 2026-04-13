from sqlalchemy import BigInteger, Column, DateTime, Integer, Numeric, String, Text, func

from app.db import Base


class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(BigInteger, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    user_message = Column(Text, nullable=False)
    bot_reply = Column(Text, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    estimated_cost = Column(Numeric(10, 6), nullable=True)
    status = Column(String(50), nullable=False, default="success")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
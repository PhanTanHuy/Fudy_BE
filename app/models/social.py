from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import TicketStatus


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    restaurant_id: Mapped[UUID] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    driver_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("driver_profiles.id"))
    food_rating: Mapped[int] = mapped_column(
        Integer, CheckConstraint("food_rating >= 1 AND food_rating <= 5"), nullable=False
    )
    restaurant_rating: Mapped[int] = mapped_column(
        Integer, CheckConstraint("restaurant_rating >= 1 AND restaurant_rating <= 5"), nullable=False
    )
    driver_rating: Mapped[Optional[int]] = mapped_column(
        Integer, CheckConstraint("driver_rating >= 1 AND driver_rating <= 5")
    )
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    customer: Mapped["User"] = relationship(back_populates="reviews")
    order: Mapped["Order"] = relationship()

    __table_args__ = (UniqueConstraint("order_id", "customer_id", name="uq_order_customer_review"),)


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("orders.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    assigned_admin_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"))
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    reference_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

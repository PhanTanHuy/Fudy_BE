from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from geoalchemy2 import Geography
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import (
    DeliveryBatchStatus,
    DispatchOfferStatus,
    DriverApprovalStatus,
    StopStatus,
    StopType,
)


class DriverProfile(Base):
    __tablename__ = "driver_profiles"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    license_number: Mapped[str] = mapped_column(String(50), nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String(50), nullable=False)
    license_plate: Mapped[str] = mapped_column(String(20), nullable=False)
    approval_status: Mapped[DriverApprovalStatus] = mapped_column(
        Enum(DriverApprovalStatus), default=DriverApprovalStatus.PENDING, nullable=False
    )
    is_online: Mapped[bool] = mapped_column(default=False, nullable=False)

    user: Mapped["User"] = relationship(back_populates="driver_profile")
    location: Mapped[Optional["DriverLocation"]] = relationship(back_populates="driver", uselist=False)
    batches: Mapped[List["DeliveryBatch"]] = relationship(back_populates="driver")


class DriverLocation(Base):
    __tablename__ = "driver_locations"

    driver_id: Mapped[UUID] = mapped_column(
        ForeignKey("driver_profiles.id", ondelete="CASCADE"), primary_key=True
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    location = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    driver: Mapped[DriverProfile] = relationship(back_populates="location")

    __table_args__ = (Index("idx_driver_location_gist", "location", postgresql_using="gist"),)


class DeliveryBatch(Base):
    __tablename__ = "delivery_batches"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    driver_id: Mapped[UUID] = mapped_column(ForeignKey("driver_profiles.id"), nullable=False)
    status: Mapped[DeliveryBatchStatus] = mapped_column(
        Enum(DeliveryBatchStatus), default=DeliveryBatchStatus.ASSIGNED, nullable=False
    )
    estimated_duration: Mapped[Optional[int]] = mapped_column(Integer)
    total_distance: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    driver: Mapped[DriverProfile] = relationship(back_populates="batches")
    batch_orders: Mapped[List["DeliveryBatchOrder"]] = relationship(
        back_populates="batch", cascade="all, delete-orphan"
    )
    stops: Mapped[List["DeliveryStop"]] = relationship(back_populates="batch", cascade="all, delete-orphan")


class DeliveryBatchOrder(Base):
    __tablename__ = "delivery_batch_orders"

    batch_id: Mapped[UUID] = mapped_column(
        ForeignKey("delivery_batches.id", ondelete="CASCADE"), primary_key=True
    )
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    batch: Mapped[DeliveryBatch] = relationship(back_populates="batch_orders")
    order: Mapped["Order"] = relationship()


class DeliveryStop(Base):
    __tablename__ = "delivery_stops"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    batch_id: Mapped[UUID] = mapped_column(ForeignKey("delivery_batches.id", ondelete="CASCADE"), nullable=False)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    stop_type: Mapped[StopType] = mapped_column(Enum(StopType), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[StopStatus] = mapped_column(Enum(StopStatus), default=StopStatus.PENDING, nullable=False)

    batch: Mapped[DeliveryBatch] = relationship(back_populates="stops")
    order: Mapped["Order"] = relationship()


class DispatchOffer(Base):
    __tablename__ = "dispatch_offers"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    driver_id: Mapped[UUID] = mapped_column(
        ForeignKey("driver_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    estimated_pickup_time: Mapped[Optional[int]] = mapped_column(Integer)
    score: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    status: Mapped[DispatchOfferStatus] = mapped_column(
        Enum(DispatchOfferStatus), default=DispatchOfferStatus.PENDING, nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    order: Mapped["Order"] = relationship()
    driver: Mapped[DriverProfile] = relationship()

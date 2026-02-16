from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String[255], nullable=False, unique=True)

class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String[255])
    created_at : Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.now())
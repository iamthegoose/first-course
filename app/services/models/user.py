from app.services.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from app.services.types.schema import Roles
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    surname: Mapped[str] = mapped_column(index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Roles] = mapped_column(default=Roles.user)

    flats = relationship("Flat", back_populates="owner")

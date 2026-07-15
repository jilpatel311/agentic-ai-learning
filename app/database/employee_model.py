from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.models import Base


class Employee(Base):

    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    employee_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    salary: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reward_points: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    work_from_home_days: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    sick_leave_remaining: Mapped[int] = mapped_column(
        Integer,
        default=6,
    )

    casual_leave_remaining: Mapped[int] = mapped_column(
        Integer,
        default=6,
    )

    privilege_leave_remaining: Mapped[int] = mapped_column(
        Integer,
        default=6,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )
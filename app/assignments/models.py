from sqlalchemy import (
    ForeignKey, DateTime, Enum, UniqueConstraint,
    )
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship,
    )
from datetime import datetime

from app.assignments.status import AssignmentStatus
from app.db.base import Base
from app.users.models import User
from app.tasks.models import Task   


class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )

    status: Mapped[AssignmentStatus] = mapped_column(
        Enum(AssignmentStatus, name="assignment_status"),
        default=AssignmentStatus.ASSIGNED,
        nullable=False,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        nullable=False,
    )

    assigned_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id],
        back_populates="assignments",
    )

    task: Mapped["Task"] = relationship(
        back_populates="assignments",
    )

    assigned_by: Mapped["User" | None] = relationship(
        foreign_keys=[assigned_by_id],
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "task_id",
            name="uq_user_task_assignment",
        ),
    )

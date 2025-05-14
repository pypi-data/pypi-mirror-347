from snakemake_logger_plugin_sqlite.models.base import Base
from snakemake_logger_plugin_sqlite.models.enums import Status

from sqlalchemy import JSON, Enum, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from datetime import datetime, timezone
from typing import Optional, Dict, Any, TYPE_CHECKING, List
import uuid

if TYPE_CHECKING:
    from snakemake_logger_plugin_sqlite.models.rule import Rule
    from snakemake_logger_plugin_sqlite.models.job import Job
    from snakemake_logger_plugin_sqlite.models.error import Error


class Workflow(Base):
    __tablename__ = "workflows"  # Using plural for consistency
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    snakefile: Mapped[Optional[str]]
    started_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    end_time: Mapped[Optional[datetime]]
    status: Mapped[Status] = mapped_column(Enum(Status), default="UNKNOWN")
    command_line: Mapped[Optional[str]]
    dryrun: Mapped[bool]
    rulegraph_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    total_job_count: Mapped[int] = mapped_column(default=0)  # from run info
    jobs_finished: Mapped[int] = mapped_column(default=0)
    rules: Mapped[list["Rule"]] = relationship(
        "Rule",
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    jobs: Mapped[list["Job"]] = relationship(
        "Job",
        back_populates="workflow",
        lazy="dynamic",  # return a query object
    )
    errors: Mapped[list["Error"]] = relationship(
        "Error",
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def progress(self) -> float:
        if self.total_job_count == 0:
            return 0.0
        return self.jobs_finished / self.total_job_count

    @classmethod
    def list_all(
        cls,
        session: Session,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
        order_by_started: bool = True,
        descending: bool = True,
    ) -> List["Workflow"]:
        """
        List all workflows in the database with optional pagination and sorting.

        Args:
            session: SQLAlchemy session to use for the query
            limit: Optional maximum number of workflows to return
            offset: Optional number of workflows to skip (for pagination)
            order_by_started: If True, order by started_at time, otherwise by id
            descending: If True, order in descending order (newest first)

        Returns:
            List of Workflow objects
        """
        query = select(cls)

        if order_by_started:
            order_column = cls.started_at
        else:
            order_column = cls.id  # type: ignore

        if descending:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column)

        if limit is not None:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return list(session.execute(query).scalars())

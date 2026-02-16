"""
Checkpointer factory for the Financial Approval workflow.

Provides SQLite-based persistence so that interrupted workflows
can be resumed after human review decisions.
"""

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from backend.config import CHECKPOINT_DB


def create_checkpointer() -> SqliteSaver:
    """
    Create a SQLite checkpointer for workflow persistence.

    The checkpointer stores graph state at each node transition,
    enabling the interrupt/resume pattern for human-in-the-loop.

    Returns:
        SqliteSaver: Configured SQLite checkpointer instance
    """
    conn = sqlite3.connect(CHECKPOINT_DB, check_same_thread=False)
    return SqliteSaver(conn)

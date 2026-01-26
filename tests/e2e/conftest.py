"""
E2E (End-to-End) test configuration.
Provides fixtures for API testing with full application stack.

Note: All common fixtures (db, auth, clients, data) are automatically
available from the root tests/conftest.py through pytest's fixture discovery.
"""

import pytest
import pytest_asyncio
from sqlalchemy import text
from tests.fixtures.db import get_base


@pytest_asyncio.fixture(autouse=True)
async def _clean_db_after_e2e_test(async_engine):
    """
    Automatically cleans up the database after each E2E test.

    This is an autouse fixture that applies to all tests in the E2E suite.
    It deletes all data from all tables after each test, ensuring test isolation.
    """
    yield

    Base = get_base()
    tables = reversed(Base.metadata.sorted_tables)

    async with async_engine.connect() as conn:
        await conn.begin()
        for table in tables:
            await conn.execute(text(f"DELETE FROM {table.name}"))
        await conn.commit()
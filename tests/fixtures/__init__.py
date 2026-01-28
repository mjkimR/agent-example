"""
Centralized fixtures package.
Import all fixtures from this package for easy access.
"""
from tests.fixtures.db import (
    event_loop_policy,
    async_engine,
    session_maker_fixture,
    session_fixture,
)
from tests.fixtures.clients import (
    AsyncClientWithJson,
    app_fixture,
    client_fixture,
    unauthenticated_client_fixture,
)

__all__ = [
    # Database fixtures
    "event_loop_policy",
    "async_engine",
    "session_maker_fixture",
    "session_fixture",
    # Client fixtures
    "AsyncClientWithJson",
    "app_fixture",
    "client_fixture",
    "unauthenticated_client_fixture",
]

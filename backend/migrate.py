"""Apply the database migrations from the migrations folder.

Runs in the container before the app starts, applied migrations are tracked
in the migrations_log collection, so this is a no-op if everything is applied.
Run `uv run python migrate.py backward` to roll the newest migration back.
"""

import asyncio
import sys
from pathlib import Path

from beanie.executors.migrate import MigrationSettings, run_migrate
from environment import SETTINGS


def main() -> None:
    direction = "BACKWARD" if "backward" in sys.argv[1:] else "FORWARD"
    distance = 1 if direction == "BACKWARD" else 0  # backward rolls back one step, forward applies all
    settings = MigrationSettings(
        direction=direction,
        distance=distance,
        connection_uri=SETTINGS.atlas_uri,
        database_name=SETTINGS.database_name,
        path=Path(__file__).parent / "migrations",
        # ponytail: no transactions, the local standalone mongo does not support them
        use_transaction=False,
    )
    asyncio.run(run_migrate(settings))


if __name__ == "__main__":
    main()

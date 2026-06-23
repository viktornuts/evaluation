from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cpt_eval.sqlite"
SCHEMA = ROOT / "db" / "schema.sql"
SEED = ROOT / "db" / "seed.sql"
CRITERION_TARGETS = ROOT / "db" / "criterion_targets.sql"


def run_script(connection: sqlite3.Connection, path: Path) -> None:
    connection.executescript(path.read_text(encoding="utf-8"))


def init_db(db_path: Path, reset: bool) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if reset and db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        run_script(connection, SCHEMA)
        run_script(connection, SEED)
        run_script(connection, CRITERION_TARGETS)
        connection.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the CPT eval SQLite database.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database file.")
    parser.add_argument("--reset", action="store_true", help="Delete the existing database before initialization.")
    args = parser.parse_args()

    init_db(args.db, args.reset)
    print(f"Initialized database: {args.db}")


if __name__ == "__main__":
    main()

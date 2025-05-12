# taskiq-postgres

PostgreSQL integration for Taskiq.

## Installation

Depend on your preferred PostgreSQL driver, you can install this library:

```bash
# with asyncpg
pip install taskiq-postgres[asyncpg]

# with psqlpy
pip install taskiq-postgres[psqlpy]

# with aiopg
pip install taskiq-postgres[aiopg]
```

## Usage

Simple example of usage with asyncpg:

```python
# broker.py
import asyncio

from taskiq_pg.asyncpg import AsyncpgResultBackend, AsyncpgBroker

result_backend = AsyncpgResultBackend(
    dsn="postgres://postgres:postgres@localhost:5432/postgres",
)

broker = AsyncpgBroker(
    dsn="postgres://postgres:postgres@localhost:5432/postgres",
).with_result_backend(result_backend)


@broker.task
async def best_task_ever() -> None:
    """Solve all problems in the world."""
    await asyncio.sleep(5.5)
    print("All problems are solved!")


async def main():
    await broker.startup()
    task = await best_task_ever.kiq()
    print(await task.wait_result())
    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
```


## Motivation

There are too many libraries for PostgreSQL and Taskiq integration. Although they have different view on interface and different functionality. 
To address this issue I created this library with a common interface for most popular PostgreSQL drivers that handle similarity across functionality of result backends and brokers.

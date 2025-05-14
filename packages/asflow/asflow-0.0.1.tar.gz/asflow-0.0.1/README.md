# AsFlow

A lightweight workflow runner for simple ETL (Extract-Transform-Load) pipelines.

Tasks are defined as async functions and executed as a single script. A workflow can be embedded in any Python projects, such as Jupyter notebooks or Streamlit dashboards, without external servers or databases.

![ScreenRecording](docs/assets/img/ScreenRecording.webp)

Features:
- Pure Python, single process; designed for seamless integration with [Streamlit](https://streamlit.io)
- Use `asyncio` for parallelism with limited concurrent access to remote services
- Use [Rich](https://rich.readthedocs.io) for logging and progress output
- Use [pandas](https://pandas.pydata.org) or [polars](https://pola.rs) for data manipulation
- Integration with [joblib](https://joblib.readthedocs.io) for data persistence

## Installation

```
% pip install asflow
```

## Getting Started

The first function (`extract()`) prepares raw data. You might retrieve data from API servers or databases. This is an I/O-bound operation, where you can use asyncio for parallelism.

The second function (`transform()`) converts the collected data into a dataframe.  All data of the same type can be concatenated into a single object.

We can use the `@flow.task` decorator to turn these functions into ASFlow tasks:

```python
import asyncio
import pandas as pd
from asflow import flow

# extract task (raw data)
@flow.task
async def extract(word):
    await asyncio.sleep(1)
    return {"word": word, "count": 1}

# transform task (create a dataframe)
@flow.task
async def transform(data):
    return pd.DataFrame(data)

async def main():
    words = ["Hello", "World"]

    # Extract (parallel)
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(extract(word)) for word in words]

    # Transform
    df = await transform(await asyncio.gather(*tasks))
    print(df)

if __name__ == "__main__":
    asyncio.run(main())
```

```
% python main.py
[12:49:06] Task extract('Hello') finished in 1.00s
           Task extract('World') finished in 1.01s
           Task transform([{'word': 'Hello', 'count': 1}, ...]) finished in 0.00s
    word  count
0  Hello      1
1  World      1
```

The decorator is a thin wrapper around async functions to memoize the results, just like `functools.cache`, `joblib.Memory.cache`, or `streamlit.store`, with some additional features for data pipeline.

Other than the additional logging, this change does nothing special. A task does not store data unless you explicitly tell it how and where to do so.

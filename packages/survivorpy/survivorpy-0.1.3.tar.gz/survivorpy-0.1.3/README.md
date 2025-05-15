# SurvivorPy

[![PyPI Downloads](https://static.pepy.tech/badge/survivorpy)](https://pepy.tech/projects/survivorpy)
[![PyPI Version](https://img.shields.io/pypi/v/survivorpy.svg)](https://pypi.org/project/survivorpy/)
[![Python Versions](https://img.shields.io/pypi/pyversions/survivorpy.svg)](https://pypi.org/project/survivorpy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/jonnycomes/survivorpy/survivorpy-tests.yml?branch=main)](https://github.com/jonnycomes/survivorpy/actions)
[![Last Commit](https://img.shields.io/github/last-commit/jonnycomes/survivorpy.svg)](https://github.com/jonnycomes/survivorpy/commits/main)


SurvivorPy is a Python wrapper of the data from the R package [survivoR](https://github.com/doehm/survivoR). It enables Python coders easy access to clean, structured data on contestants, seasons, episodes, votes, and more from the reality show *Survivor*—directly from Python, using familiar `pandas` dataframes.

SurvivorPy syncs its data with survivoR on a daily basis, ensuring the data reflects recent updates to the survivoR package.

## Installation

You can install SurvivorPy from PyPI:

```bash
pip install survivorpy
```

## Usage

There are a couple of different ways to access Survivor data with `survivorpy`, depending on your preferences and needs. In both cases, the tables are provided as `pandas` DataFrames.


### Import a table directly

If you know the name of the table you want, you can import it directly:

```python
from survivorpy import castaways

castaways.head()
```

### See all available tables
To see what's available, use the `TABLE_NAMES` constant:

```python
from survivorpy import TABLE_NAMES

print(TABLE_NAMES)
# [..., 'castaways', ...]
```

### Using the `load()` function
`survivorpy` provides a `load()` function which gives an alternative way to access the tables:

```python
import survivorpy as sv

df = sv.load('castaways')
df.head()
```

No matter which method you choose, you’ll get rich Survivor data, neatly packaged and ready to explore with your favorite `pandas` tools.


### Keeping data up to date

On first import, `survivorpy` fetches and caches all the tables locally, which might feel a bit slow. The upside is that after this initial step, loading data—whether via `load()` or by importing tables directly—is fast and works offline.  
To update your local cache with the latest data from the source (typically updated daily to match the R package [`survivoR`](https://github.com/doehm/survivoR)), use:

```python
sv.refresh_data()
```

To see a summary of what changed during the update (e.g. which tables were modified), pass `verbose=True`:

```python
sv.refresh_data(verbose=True)
```

If you just want to see the last time your data was synced, use the `LAST_SYNCED` constant to get a UTC timestamp:

```python
sv.LAST_SYNCED
# e.g., '2025-04-25T18:42:07.235Z'
```

## Data Source and Attribution

This package provides Python access to data from the [survivoR](https://github.com/doehm/survivoR) package by Daniel Oehm and contributors. We’re grateful to the folks at survivoR for maintaining such a rich and well-structured dataset.

The original data is licensed under the MIT License, and we preserve that license and attribution in accordance with its terms.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/jonnycomes/survivorpy/blob/main/LICENSE) file for details.

## Contributing

Got ideas or spot a bug? Feel free to open an [issue](https://github.com/jonnycomes/survivorpy/issues) or a [pull request](https://github.com/jonnycomes/survivorpy/pulls) — contributions of all kinds are welcome!



